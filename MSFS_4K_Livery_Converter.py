#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MSFS 2024 Livery 4K Converter

A small Windows GUI that batch-resizes large texture files using Microsoft's
DirectXTex texconv utility. Original files are never modified.
"""
from __future__ import annotations

import os
import queue
import shutil
import struct
import subprocess
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Optional

try:
    from PIL import Image
except ImportError:
    Image = None  # DDS header reading still works without Pillow.

APP_TITLE = "MSFS 2024 – Livery 4K Converter"
SUPPORTED_EXTENSIONS = {
    ".dds", ".png", ".tga", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"
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
        self.root.geometry("900x690")
        self.root.minsize(760, 590)

        self.events: queue.Queue[tuple] = queue.Queue()
        self.worker: Optional[threading.Thread] = None
        self.cancel_event = threading.Event()

        self.source_var = tk.StringVar()
        self.target_var = tk.StringVar()
        self.texconv_var = tk.StringVar(value=find_texconv())
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
            text="Unterstützte Formate: DDS, PNG, TGA, JPG/JPEG, BMP und TIFF.",
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
            self._append_log("Hinweis: texconv.exe wurde nicht gefunden. Bitte die Datei auswählen oder installieren.")
        if Image is None:
            self._append_log("Hinweis: Pillow ist nicht installiert. DDS-Dateien funktionieren; Rasterdateien benötigen Pillow.")

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
        if not texconv_text or not Path(texconv_text).is_file():
            messagebox.showerror(
                "texconv.exe fehlt",
                "Microsoft DirectXTex texconv wurde nicht gefunden.\n\n"
                "Installation über PowerShell/Eingabeaufforderung:\n"
                "winget install Microsoft.DirectXTex.Texconv\n\n"
                "Danach texconv.exe hier auswählen.",
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
            args=(source, target, Path(texconv_text), max_size),
            daemon=True,
        )
        self.worker.start()

    def cancel(self) -> None:
        self.cancel_event.set()
        self.status_var.set("Abbruch angefordert – aktueller Verarbeitungsschritt wird beendet …")
        self.cancel_button.configure(state="disabled")

    def _worker_main(self, source: Path, target: Path, texconv: Path, max_size: int) -> None:
        try:
            files: list[Path] = []
            target_resolved = target.resolve()
            for current_root, dirs, names in os.walk(source):
                current_path = Path(current_root).resolve()
                # Do not rescan output when it is placed inside the source tree.
                dirs[:] = [d for d in dirs if not (current_path / d).resolve().is_relative_to(target_resolved)]
                for name in names:
                    candidate = Path(current_root) / name
                    if candidate.suffix.lower() in SUPPORTED_EXTENSIONS:
                        files.append(candidate)

            self.events.put(("log", f"Gefundene unterstützte Dateien: {len(files)}"))
            prepared: list[tuple[Path, int, int, int, int]] = []
            unreadable = 0
            for file_path in files:
                if self.cancel_event.is_set():
                    break
                try:
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
            self.events.put(("log", f"Zu verkleinernde Texturen: {total}; nicht lesbar: {unreadable}"))
            if self.cancel_event.is_set():
                self.events.put(("finished", "Abgebrochen.", 0, 0, 0))
                return
            if total == 0:
                self.events.put(("finished", "Keine Texturen über der eingestellten Kantenlänge gefunden.", 0, 0, unreadable))
                return

            converted = 0
            failed = 0
            for index, (src, old_w, old_h, new_w, new_h) in enumerate(prepared, start=1):
                if self.cancel_event.is_set():
                    break
                relative = src.relative_to(source)
                destination_folder = target / relative.parent
                destination_folder.mkdir(parents=True, exist_ok=True)
                texconv_format, generated_ext = TEXCONV_FORMAT[src.suffix.lower()]
                generated = destination_folder / f"{src.stem}{generated_ext}"
                desired = destination_folder / src.name

                command = [
                    str(texconv),
                    "-nologo",
                    "-y",
                    "-if", "FANT",
                    "-w", str(new_w),
                    "-h", str(new_h),
                    "-ft", texconv_format,
                    "-o", str(destination_folder),
                ]
                if src.suffix.lower() == ".dds":
                    # Regenerate the complete DDS mip chain after resizing.
                    command.extend(["-m", "0"])
                command.append(str(src))

                self.events.put(("status", f"{index}/{total}: {src.name} ({old_w}×{old_h} → {new_w}×{new_h})"))
                try:
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

                    # Preserve the original extension's spelling (e.g. .DDS / .jpeg).
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

            if self.cancel_event.is_set():
                result_text = "Abgebrochen."
            else:
                result_text = "Fertig."
            self.events.put(("finished", result_text, converted, failed, unreadable))
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
                    _, result_text, converted, failed, unreadable = event
                    self.status_var.set(f"{result_text} Erfolgreich: {converted} | Fehler: {failed} | Nicht lesbar: {unreadable}")
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
