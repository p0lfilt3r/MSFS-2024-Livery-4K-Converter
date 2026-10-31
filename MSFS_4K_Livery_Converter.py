#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MSFS 2024 Livery 4K Converter

A small Windows GUI that batch-resizes large texture files using Microsoft's
DirectXTex texconv utility. Original files are never modified.
"""
from __future__ import annotations

import json
import os
import queue
import shutil
import struct
import subprocess
import tempfile
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from dataclasses import dataclass
from typing import Optional

try:
    from PIL import Image
except ImportError:
    Image = None  # DDS header reading still works without Pillow.

APP_TITLE = "MSFS 2024 – Livery 4K Converter"
SUPPORTED_EXTENSIONS = {
    ".dds", ".png", ".tga", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".ktx2"
}
# texconv's output extension may be normalized for some WIC formats.
TEXCONV_FORMAT = {
    ".dds": ("dds", ".dds"),
    ".png": ("png", ".png"),
    ".tga": ("tga", ".tga"),
    ".jpg": ("jpg", ".jpg"),
    ".jpeg": ("jpg", ".jpg"),
    ".bmp": ("bmp", ".bmp"),
    ".tif": ("tif", ".tif"),
    ".tiff": ("tif", ".tif"),
}


def find_texconv() -> str:
    """Try PATH and common winget package locations."""
    found = shutil.which("texconv.exe") or shutil.which("texconv")
    if found:
        return found

    local = os.environ.get("LOCALAPPDATA")
    if local:
        packages = Path(local) / "Microsoft" / "WinGet" / "Packages"
        if packages.exists():
            try:
                for candidate in packages.rglob("texconv.exe"):
                    if any("DirectXTex" in part for part in candidate.parts):
                        return str(candidate)
            except OSError:
                pass
    return ""


def find_ktx() -> str:
    """Find the Khronos KTX-Software command line tool."""
    found = shutil.which("ktx.exe") or shutil.which("ktx")
    if found:
        return found

    roots = []
    for env_name in ("ProgramFiles", "ProgramW6432", "LOCALAPPDATA"):
        value = os.environ.get(env_name)
        if value:
            roots.append(Path(value))
    for root in roots:
        for relative in (
            Path("KTX-Software") / "bin" / "ktx.exe",
            Path("Khronos") / "KTX-Software" / "bin" / "ktx.exe",
        ):
            candidate = root / relative
            if candidate.is_file():
                return str(candidate)
        try:
            for candidate in root.glob("KTX-Software*/bin/ktx.exe"):
                if candidate.is_file():
                    return str(candidate)
        except OSError:
            pass
    return ""


@dataclass(frozen=True)
class KTX2Header:
    width: int
    height: int
    vk_format: int
    depth: int
    layers: int
    faces: int
    levels: int
    supercompression: int


KTX2_IDENTIFIER = b"\xABKTX 20\xBB\r\n\x1A\n"


def read_ktx2_header(path: Path) -> KTX2Header:
    """Read the fixed KTX2 header without decoding the texture payload."""
    with path.open("rb") as stream:
        header = stream.read(80)
    if len(header) < 80 or header[:12] != KTX2_IDENTIFIER:
        raise ValueError("Ungültiger oder nicht unterstützter KTX2-Header")
    values = struct.unpack_from("<9I", header, 12)
    vk_format, _type_size, width, height, depth, layers, faces, levels, supercompression = values
    if width <= 0 or height <= 0:
        raise ValueError("KTX2-Datei enthält ungültige Abmessungen")
    return KTX2Header(width, height, vk_format, depth, layers, faces, levels, supercompression)


def run_tool(command: list[str], tool_name: str) -> subprocess.CompletedProcess:
    """Run an external texture tool and return useful UTF-8 diagnostics."""
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        check=False,
    )
    if result.returncode != 0:
        details = (result.stdout or "").strip().replace("\r", " ")
        if len(details) > 1200:
            details = details[-1200:]
        raise RuntimeError(details or f"{tool_name} beendete sich mit Code {result.returncode}")
    return result


def get_ktx_info(ktx: Path, source: Path) -> dict:
    result = run_tool([str(ktx), "info", "--format", "json", str(source)], "ktx info")
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"ktx info lieferte keine gültige JSON-Information: {exc}") from exc
    if not data.get("valid", True):
        messages = data.get("messages", [])
        details = "; ".join(item.get("message", "Ungültige KTX2-Datei") for item in messages)
        raise RuntimeError(details or "KTX2-Datei ist laut ktx info ungültig")
    return data


def ktx2_format_name(vk_format: object) -> str:
    """Normalize the vkFormat value returned by ktx info."""
    if isinstance(vk_format, str):
        name = vk_format.upper()
        return name if name.startswith("VK_FORMAT_") else f"VK_FORMAT_{name}"
    common = {
        0: "VK_FORMAT_UNDEFINED",
        9: "VK_FORMAT_R8_UNORM",
        16: "VK_FORMAT_R8G8_UNORM",
        23: "VK_FORMAT_R8G8B8_UNORM",
        29: "VK_FORMAT_R8G8B8_SRGB",
        37: "VK_FORMAT_R8G8B8A8_UNORM",
        43: "VK_FORMAT_R8G8B8A8_SRGB",
    }
    try:
        return common[int(vk_format)]
    except (KeyError, TypeError, ValueError):
        raise RuntimeError(f"Unbekanntes Vulkan-Texturformat (vkFormat={vk_format})")


def convert_ktx2(ktx: Path, source: Path, destination: Path, width: int, height: int) -> None:
    """Resize a standard 2D KTX2 file and regenerate its mip chain."""
    header = read_ktx2_header(source)
    if header.supercompression == 65536:
        raise RuntimeError(
            "MSFS-Sonderkomprimierung 65536 erkannt. Diese proprietäre KTX2-Variante "
            "kann das öffentliche Khronos-KTX-Werkzeug nicht lesen."
        )
    if header.supercompression not in (0, 1, 2, 3):
        raise RuntimeError(
            f"Nicht unterstützte KTX2-Superkomprimierung {header.supercompression}. "
            "Die Datei wurde unverändert übersprungen."
        )
    if header.depth != 0 or header.layers != 0 or header.faces != 1:
        raise RuntimeError("Nur normale 2D-KTX2-Texturen ohne Array, Cubemap oder 3D-Daten werden unterstützt.")

    info = get_ktx_info(ktx, source)
    header_info = info.get("header", {})
    dfd_blocks = info.get("dataFormatDescriptor", {}).get("blocks", [])
    if not dfd_blocks:
        raise RuntimeError("KTX2-Datei enthält keinen lesbaren Data Format Descriptor.")
    dfd = dfd_blocks[0]
    color_model = str(dfd.get("colorModel", "")).upper()
    transfer = str(dfd.get("transferFunction", "")).upper()
    flags = [str(value).upper() for value in dfd.get("flags", [])]
    if any("ALPHA_PREMULTIPLIED" in flag for flag in flags):
        raise RuntimeError("Premultipliziertes Alpha wird derzeit nicht verlustfrei neu aufgebaut; Datei übersprungen.")

    if transfer in ("KHR_DF_TRANSFER_SRGB", "2"):
        is_srgb = True
    elif transfer in ("KHR_DF_TRANSFER_LINEAR", "1"):
        is_srgb = False
    else:
        raise RuntimeError(f"Transferfunktion {transfer or 'unbekannt'} wird nicht unterstützt.")

    format_name = ktx2_format_name(header_info.get("vkFormat", header.vk_format))
    key_values = info.get("keyValueData", {})
    orientation = key_values.get("KTXorientation", "rd")
    swizzle = key_values.get("KTXswizzle")
    color_primaries = str(dfd.get("colorPrimaries", "")).upper()

    with tempfile.TemporaryDirectory(prefix="msfs_ktx2_") as temp_name:
        temp = Path(temp_name)
        extracted = temp / "source.png"
        output = temp / "resized.ktx2"
        extract_command = [str(ktx), "extract", "--level", "0"]
        if format_name == "VK_FORMAT_UNDEFINED":
            if ("ETC1S" in color_model and header.supercompression == 1) or "UASTC" in color_model:
                # Request a predictable four-channel PNG for the universal codecs.
                extract_command.extend(["--transcode", "rgba8"])
        extract_command.extend([str(source), str(extracted)])
        run_tool(extract_command, "ktx extract")
        if not extracted.is_file():
            raise RuntimeError("ktx extract hat keine PNG-Datei erzeugt.")

        command = [str(ktx), "create"]
        if format_name == "VK_FORMAT_UNDEFINED":
            # BasisLZ (ETC1S) and UASTC have no Vulkan format in the KTX2 header.
            if "ETC1S" in color_model and header.supercompression == 1:
                command.extend(["--format", "R8G8B8A8_SRGB" if is_srgb else "R8G8B8A8_UNORM", "--encode", "basis-lz"])
            elif "UASTC" in color_model:
                command.extend(["--format", "R8G8B8A8_SRGB" if is_srgb else "R8G8B8A8_UNORM", "--encode", "uastc-ldr-4x4", "--uastc-quality", "2"])
                if header.supercompression == 2:
                    command.extend(["--zstd", "18"])
            else:
                raise RuntimeError(
                    f"KTX2-Format VK_FORMAT_UNDEFINED mit Farbmodell {color_model or 'unbekannt'} "
                    "kann nicht sicher neu erstellt werden."
                )
        else:
            # Preserve standard 8-bit uncompressed and ASTC formats. Other GPU block formats
            # cannot be re-encoded from PNG by the public KTX CLI with format fidelity.
            is_astc = format_name.startswith("VK_FORMAT_ASTC_") and ("_UNORM_BLOCK" in format_name or "_SRGB_BLOCK" in format_name)
            is_8bit_color = format_name in {
                "VK_FORMAT_R8G8B8_UNORM", "VK_FORMAT_R8G8B8_SRGB",
                "VK_FORMAT_R8G8B8A8_UNORM", "VK_FORMAT_R8G8B8A8_SRGB",
            }
            if not (is_astc or is_8bit_color):
                raise RuntimeError(
                    f"Das KTX2-Pixel-Format {format_name} kann mit dem öffentlichen KTX-Werkzeug "
                    "nicht formatgetreu aus PNG neu komprimiert werden. Datei übersprungen."
                )
            command.extend(["--format", format_name])
            if header.supercompression == 2:
                command.extend(["--zstd", "18"])
            elif header.supercompression == 3:
                command.extend(["--zlib", "9"])

        command.extend([
            "--width", str(width), "--height", str(height),
            "--generate-mipmap", "--mipmap-filter", "lanczos4",
        ])
        if not is_srgb:
            command.extend(["--assign-tf", "linear"])
        primaries_map = {
            "KHR_DF_PRIMARIES_BT709": "bt709",
            "KHR_DF_PRIMARIES_SRGB": "srgb",
            "KHR_DF_PRIMARIES_BT2020": "bt2020",
            "KHR_DF_PRIMARIES_DISPLAYP3": "displayp3",
            "KHR_DF_PRIMARIES_ADOBERGB": "adobergb",
        }
        if color_primaries in primaries_map:
            command.extend(["--assign-primaries", primaries_map[color_primaries]])
        if orientation in ("rd", "rdi"):
            command.extend(["--assign-texcoord-origin", "top-left"])
        elif orientation in ("ru", "rui"):
            command.extend(["--assign-texcoord-origin", "bottom-left"])
        if isinstance(swizzle, str) and len(swizzle) == 4 and all(ch in "rgba01" for ch in swizzle.lower()):
            command.extend(["--swizzle", swizzle.lower()])
        command.extend([str(extracted), str(output)])
        run_tool(command, "ktx create")
        if not output.is_file() or output.stat().st_size == 0:
            raise RuntimeError("ktx create hat keine gültige Ausgabedatei erzeugt.")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(output, destination)


def read_dds_dimensions(path: Path) -> tuple[int, int]:
    """Read width and height from the standard DDS_HEADER."""
    with path.open("rb") as stream:
        header = stream.read(128)
    if len(header) < 128 or header[:4] != b"DDS ":
        raise ValueError("Ungültiger oder nicht unterstützter DDS-Header")
    header_size = struct.unpack_from("<I", header, 4)[0]
    if header_size != 124:
        raise ValueError("Unbekannte DDS-Header-Version")
    height = struct.unpack_from("<I", header, 12)[0]
    width = struct.unpack_from("<I", header, 16)[0]
    if width <= 0 or height <= 0:
        raise ValueError("DDS-Datei enthält ungültige Abmessungen")
    return width, height


def get_image_dimensions(path: Path) -> tuple[int, int]:
    if path.suffix.lower() == ".dds":
        return read_dds_dimensions(path)
    if path.suffix.lower() == ".ktx2":
        header = read_ktx2_header(path)
        return header.width, header.height
    if Image is None:
        raise RuntimeError(
            "Für Nicht-DDS-Dateien fehlt Pillow. Installiere es mit: python -m pip install Pillow"
        )
    with Image.open(path) as image:
        return image.size


class ConverterApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("940x760")
        self.root.minsize(800, 650)

        self.events: queue.Queue[tuple] = queue.Queue()
        self.worker: Optional[threading.Thread] = None
        self.cancel_event = threading.Event()

        self.source_var = tk.StringVar()
        self.target_var = tk.StringVar()
        self.texconv_var = tk.StringVar(value=find_texconv())
        self.ktx_var = tk.StringVar(value=find_ktx())
        self.max_size_var = tk.StringVar(value="4096")
        self.status_var = tk.StringVar(value="Bereit")
        self.progress_var = tk.DoubleVar(value=0)

        self._build_ui()
        self.root.after(120, self._process_events)

    def _build_ui(self) -> None:
        style = ttk.Style()
        try:
            style.theme_use("vista" if os.name == "nt" else "clam")
        except tk.TclError:
            pass
        style.configure("Title.TLabel", font=("Segoe UI", 17, "bold"))
        style.configure("Info.TLabel", font=("Segoe UI", 9))
        style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), padding=(14, 8))

        outer = ttk.Frame(self.root, padding=18)
        outer.pack(fill="both", expand=True)

        ttk.Label(outer, text="MSFS 2024 – Livery 4K Converter", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            outer,
            text=(
                "Große Lackierungs-Texturen stapelweise verkleinern. "
                "Die Originaldateien bleiben unverändert."
            ),
            style="Info.TLabel",
        ).pack(anchor="w", pady=(4, 16))

        paths = ttk.LabelFrame(outer, text="Ordner und Werkzeug", padding=12)
        paths.pack(fill="x")
        self._path_row(paths, 0, "Quellordner:", self.source_var, self._choose_source, "Ordner auswählen …")
        self._path_row(paths, 1, "Zielordner:", self.target_var, self._choose_target, "Ordner auswählen …")
        self._path_row(paths, 2, "texconv.exe:", self.texconv_var, self._choose_texconv, "Datei auswählen …")
        self._path_row(paths, 3, "ktx.exe:", self.ktx_var, self._choose_ktx, "Datei auswählen …")

        settings = ttk.LabelFrame(outer, text="Einstellungen", padding=12)
        settings.pack(fill="x", pady=(12, 0))
        row = ttk.Frame(settings)
        row.pack(fill="x")
        ttk.Label(row, text="Maximale Kantenlänge:").pack(side="left")
        size_entry = ttk.Entry(row, textvariable=self.max_size_var, width=9)
        size_entry.pack(side="left", padx=(8, 6))
        ttk.Label(row, text="Pixel (Standard: 4096 = 4K)").pack(side="left")
        ttk.Label(
            settings,
            text=(
                "Texturen, deren Breite oder Höhe größer ist, werden proportional verkleinert. "
                "Das Seitenverhältnis bleibt erhalten. Kleinere Texturen werden übersprungen."
            ),
            style="Info.TLabel",
            wraplength=820,
        ).pack(anchor="w", pady=(8, 0))

        note = ttk.Frame(outer)
        note.pack(fill="x", pady=(10, 0))
        ttk.Label(
            note,
            text="Unterordner werden automatisch einbezogen; die Ordnerstruktur und Dateinamen bleiben erhalten.",
            style="Info.TLabel",
            wraplength=820,
        ).pack(anchor="w")
        ttk.Label(
            note,
            text=(
                "KTX2: Standarddateien werden mit der Khronos KTX-Software neu aufgebaut. "
                "Proprietäre MSFS-Komprimierungen (z. B. 65536) werden erkannt und übersprungen."
            ),
            style="Info.TLabel",
            wraplength=820,
        ).pack(anchor="w", pady=(3, 0))
        ttk.Label(
            note,
            text="Unterstützte Formate: DDS, PNG, TGA, JPG/JPEG, BMP, TIFF und standardkonformes KTX2.",
            style="Info.TLabel",
        ).pack(anchor="w", pady=(3, 0))

        progress_frame = ttk.LabelFrame(outer, text="Fortschritt", padding=12)
        progress_frame.pack(fill="both", expand=True, pady=(12, 0))
        self.progress = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress.pack(fill="x")
        ttk.Label(progress_frame, textvariable=self.status_var, style="Info.TLabel").pack(anchor="w", pady=(6, 8))

        log_frame = ttk.Frame(progress_frame)
        log_frame.pack(fill="both", expand=True)
        self.log = tk.Text(log_frame, height=12, wrap="word", state="disabled", font=("Consolas", 9))
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log.yview)
        self.log.configure(yscrollcommand=scrollbar.set)
        self.log.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        actions = ttk.Frame(outer)
        actions.pack(fill="x", pady=(14, 0))
        self.start_button = ttk.Button(actions, text="Konvertierung starten", style="Action.TButton", command=self.start)
        self.start_button.pack(side="left")
        self.cancel_button = ttk.Button(actions, text="Abbrechen", command=self.cancel, state="disabled")
        self.cancel_button.pack(side="left", padx=(8, 0))
        ttk.Button(actions, text="Schließen", command=self.root.destroy).pack(side="right")

        if not self.texconv_var.get():
            self._append_log("Hinweis: texconv.exe wurde nicht gefunden. Für DDS und normale Bilddateien auswählen/installieren.")
        if not self.ktx_var.get():
            self._append_log("Hinweis: ktx.exe wurde nicht gefunden. Für KTX2-Dateien die Khronos KTX-Software installieren und hier auswählen.")
        if Image is None:
            self._append_log("Hinweis: Pillow ist nicht installiert. Installiere es mit: python -m pip install Pillow")

    def _path_row(self, parent, row_index, label, variable, command, button_text) -> None:
        ttk.Label(parent, text=label, width=14).grid(row=row_index, column=0, sticky="w", pady=4)
        entry = ttk.Entry(parent, textvariable=variable)
        entry.grid(row=row_index, column=1, sticky="ew", padx=(6, 8), pady=4)
        ttk.Button(parent, text=button_text, command=command).grid(row=row_index, column=2, pady=4)
        parent.columnconfigure(1, weight=1)

    def _choose_source(self) -> None:
        selected = filedialog.askdirectory(title="Ordner mit den Lackierungs-Texturen auswählen")
        if selected:
            self.source_var.set(selected)
            src = Path(selected)
            if not self.target_var.get().strip():
                self.target_var.set(str(src.parent / f"{src.name}_4K"))

    def _choose_target(self) -> None:
        selected = filedialog.askdirectory(title="Zielordner für die 4K-Texturen auswählen")
        if selected:
            self.target_var.set(selected)

    def _choose_texconv(self) -> None:
        selected = filedialog.askopenfilename(
            title="texconv.exe auswählen",
            filetypes=[("texconv.exe", "texconv.exe"), ("Programme", "*.exe"), ("Alle Dateien", "*.*")],
        )
        if selected:
            self.texconv_var.set(selected)

    def _choose_ktx(self) -> None:
        selected = filedialog.askopenfilename(
            title="ktx.exe (Khronos KTX-Software) auswählen",
            filetypes=[("ktx.exe", "ktx.exe"), ("Programme", "*.exe"), ("Alle Dateien", "*.*")],
        )
        if selected:
            self.ktx_var.set(selected)

    def _append_log(self, line: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", line + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def start(self) -> None:
        if self.worker and self.worker.is_alive():
            return
        source_text = self.source_var.get().strip()
        target_text = self.target_var.get().strip()
        texconv_text = self.texconv_var.get().strip()
        ktx_text = self.ktx_var.get().strip()
        if not source_text or not Path(source_text).is_dir():
            messagebox.showerror("Quellordner fehlt", "Bitte einen gültigen Quellordner auswählen.")
            return
        if not target_text:
            messagebox.showerror("Zielordner fehlt", "Bitte einen Zielordner auswählen.")
            return
        source = Path(source_text).resolve()
        target = Path(target_text).resolve()
        if source == target:
            messagebox.showerror("Ungültiger Zielordner", "Quell- und Zielordner dürfen nicht identisch sein.")
            return

        present_extensions = set()
        try:
            for current_root, dirs, names in os.walk(source):
                current_path = Path(current_root).resolve()
                dirs[:] = [d for d in dirs if not (current_path / d).resolve().is_relative_to(target)]
                for name in names:
                    ext = Path(name).suffix.lower()
                    if ext in SUPPORTED_EXTENSIONS:
                        present_extensions.add(ext)
        except OSError as exc:
            messagebox.showerror("Ordner kann nicht gelesen werden", str(exc))
            return

        needs_ktx = ".ktx2" in present_extensions
        needs_texconv = any(ext != ".ktx2" for ext in present_extensions)
        texconv_path = Path(texconv_text) if texconv_text and Path(texconv_text).is_file() else None
        ktx_path = Path(ktx_text) if ktx_text and Path(ktx_text).is_file() else None
        if needs_texconv and texconv_path is None:
            messagebox.showerror(
                "texconv.exe fehlt",
                "Für DDS und normale Bilddateien wird Microsoft DirectXTex texconv benötigt.\n\n"
                "Installation über PowerShell/Eingabeaufforderung:\n"
                "winget install Microsoft.DirectXTex.Texconv\n\n"
                "Danach texconv.exe hier auswählen.",
            )
            return
        if needs_ktx and ktx_path is None:
            messagebox.showerror(
                "ktx.exe fehlt",
                "Für KTX2-Dateien wird die Khronos KTX-Software benötigt.\n\n"
                "Windows-Version herunterladen unter:\n"
                "https://github.com/KhronosGroup/KTX-Software/releases\n\n"
                "Anschließend ktx.exe hier auswählen.",
            )
            return
        try:
            max_size = int(self.max_size_var.get().strip())
            if not 256 <= max_size <= 32768:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ungültige Größe", "Die maximale Kantenlänge muss eine Zahl zwischen 256 und 32768 sein.")
            return

        self.cancel_event.clear()
        self.progress_var.set(0)
        self.status_var.set("Suche Texturen …")
        self.start_button.configure(state="disabled")
        self.cancel_button.configure(state="normal")
        self._append_log("\n" + "=" * 72)
        self._append_log(f"Start: {source}")
        self._append_log(f"Ziel:  {target}")
        self.worker = threading.Thread(
            target=self._worker_main,
            args=(source, target, texconv_path, ktx_path, max_size),
            daemon=True,
        )
        self.worker.start()

    def cancel(self) -> None:
        self.cancel_event.set()
        self.status_var.set("Abbruch angefordert – aktueller Verarbeitungsschritt wird beendet …")
        self.cancel_button.configure(state="disabled")

    def _worker_main(
        self,
        source: Path,
        target: Path,
        texconv: Optional[Path],
        ktx: Optional[Path],
        max_size: int,
    ) -> None:
        try:
            files: list[Path] = []
            target_resolved = target.resolve()
            for current_root, dirs, names in os.walk(source):
                current_path = Path(current_root).resolve()
                dirs[:] = [d for d in dirs if not (current_path / d).resolve().is_relative_to(target_resolved)]
                for name in names:
                    candidate = Path(current_root) / name
                    if candidate.suffix.lower() in SUPPORTED_EXTENSIONS:
                        files.append(candidate)

            self.events.put(("log", f"Gefundene unterstützte Dateien: {len(files)}"))
            prepared: list[tuple[Path, int, int, int, int]] = []
            unreadable = 0
            unsupported = 0
            for file_path in files:
                if self.cancel_event.is_set():
                    break
                try:
                    if file_path.suffix.lower() == ".ktx2":
                        ktx_header = read_ktx2_header(file_path)
                        if ktx_header.supercompression == 65536:
                            unsupported += 1
                            self.events.put((
                                "log",
                                f"NICHT DIREKT KONVERTIERBAR (MSFS-KTX2-Kennwert 65536): {file_path.name} "
                                "– mit MSFS Livery Toolkit als PNG extrahieren, dieses PNG hier verkleinern "
                                "und anschließend über das MSFS-SDK neu kompilieren. Original bleibt unverändert.",
                            ))
                            continue
                    width, height = get_image_dimensions(file_path)
                    if max(width, height) > max_size:
                        scale = max_size / max(width, height)
                        new_width = max(1, int(round(width * scale)))
                        new_height = max(1, int(round(height * scale)))
                        prepared.append((file_path, width, height, new_width, new_height))
                except Exception as exc:
                    unreadable += 1
                    self.events.put(("log", f"ÜBERSPRUNGEN (Abmessungen nicht lesbar): {file_path.name} – {exc}"))

            total = len(prepared)
            self.events.put(("log", f"Zu verkleinernde Texturen: {total}; nicht lesbar: {unreadable}; nicht unterstützt: {unsupported}"))
            if self.cancel_event.is_set():
                self.events.put(("finished", "Abgebrochen.", 0, 0, unreadable, unsupported))
                return
            if total == 0:
                self.events.put(("finished", "Keine unterstützte Textur über der eingestellten Kantenlänge gefunden.", 0, 0, unreadable, unsupported))
                return

            converted = 0
            failed = 0
            for index, (src, old_w, old_h, new_w, new_h) in enumerate(prepared, start=1):
                if self.cancel_event.is_set():
                    break
                relative = src.relative_to(source)
                destination_folder = target / relative.parent
                destination_folder.mkdir(parents=True, exist_ok=True)
                desired = destination_folder / src.name

                self.events.put(("status", f"{index}/{total}: {src.name} ({old_w}×{old_h} → {new_w}×{new_h})"))
                try:
                    if src.suffix.lower() == ".ktx2":
                        if ktx is None:
                            raise RuntimeError("ktx.exe fehlt.")
                        convert_ktx2(ktx, src, desired, new_w, new_h)
                    else:
                        if texconv is None:
                            raise RuntimeError("texconv.exe fehlt.")
                        texconv_format, generated_ext = TEXCONV_FORMAT[src.suffix.lower()]
                        generated = destination_folder / f"{src.stem}{generated_ext}"
                        command = [
                            str(texconv), "-nologo", "-y", "-if", "FANT",
                            "-w", str(new_w), "-h", str(new_h),
                            "-ft", texconv_format, "-o", str(destination_folder),
                        ]
                        if src.suffix.lower() == ".dds":
                            command.extend(["-m", "0"])
                        command.append(str(src))
                        result = subprocess.run(
                            command,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            text=True,
                            encoding="utf-8",
                            errors="replace",
                            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                            check=False,
                        )
                        if result.returncode != 0 or not generated.exists():
                            details = (result.stdout or "").strip().replace("\r", " ")
                            if len(details) > 700:
                                details = details[-700:]
                            raise RuntimeError(details or f"texconv beendete sich mit Code {result.returncode}")
                        if generated != desired:
                            if desired.exists():
                                desired.unlink()
                            generated.replace(desired)

                    converted += 1
                    self.events.put(("log", f"OK: {relative}  {old_w}×{old_h} → {new_w}×{new_h}"))
                except Exception as exc:
                    failed += 1
                    self.events.put(("log", f"FEHLER: {relative} – {exc}"))

                self.events.put(("progress", index, total))

            result_text = "Abgebrochen." if self.cancel_event.is_set() else "Fertig."
            self.events.put(("finished", result_text, converted, failed, unreadable, unsupported))
        except Exception as exc:
            self.events.put(("fatal", str(exc)))

    def _process_events(self) -> None:
        try:
            while True:
                event = self.events.get_nowait()
                kind = event[0]
                if kind == "log":
                    self._append_log(event[1])
                elif kind == "status":
                    self.status_var.set(event[1])
                elif kind == "progress":
                    _, current, total = event
                    self.progress_var.set(current * 100 / max(total, 1))
                elif kind == "finished":
                    _, result_text, converted, failed, unreadable, unsupported = event
                    self.status_var.set(
                        f"{result_text} Erfolgreich: {converted} | Fehler: {failed} | "
                        f"Nicht lesbar: {unreadable} | Nicht unterstützt: {unsupported}"
                    )
                    self._append_log(self.status_var.get())
                    self.start_button.configure(state="normal")
                    self.cancel_button.configure(state="disabled")
                elif kind == "fatal":
                    self.status_var.set("Abbruch wegen eines Fehlers")
                    self._append_log(f"SCHWERER FEHLER: {event[1]}")
                    self.start_button.configure(state="normal")
                    self.cancel_button.configure(state="disabled")
                    messagebox.showerror("Fehler", event[1])
        except queue.Empty:
            pass
        self.root.after(120, self._process_events)


def main() -> None:
    root = tk.Tk()
    ConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
