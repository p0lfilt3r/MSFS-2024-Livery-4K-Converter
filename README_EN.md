# MSFS 2024 – Livery 4K Converter

**[English](README_EN.md) | [Deutsch](README_DE.md)**

[![License: GPL-3.0-only](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

## Download v1.8

[Download the v1.8 GitHub source archive (ZIP)](https://github.com/p0lfilt3r/MSFS-2024-Livery-4K-Converter/archive/refs/heads/release-v1.8.zip)

A Windows desktop utility that creates a lower-resolution copy of Microsoft Flight Simulator 2024 aircraft-livery packages. It keeps the source package unchanged, copies the package structure, and resizes supported textures above a configured maximum dimension.

> **Current source snapshot:** v1.8 – original material properties preserved, recursive batch processing, and responsive window.  
> The Git history is reconstructed from seven ZIP snapshots. It includes the initial pre-KTX2 converter, a later archive labelled `v2` that adds early KTX2 processing, and the subsequent v1.3–v1.6 snapshots.

## Features in v1.8

- Batch-processes a complete livery/package folder, including subfolders.
- Copies non-texture files and preserves the directory structure.
- Resizes supported textures above the configured maximum dimension (4K by default).
- Includes DDS/KTX2 and BC7 processing paths as implemented in the supplied application versions.
- Includes selectable DirectCompute adapter acceleration for the BC7 workflow where supported by the installed tool and GPU.
- Can optionally invoke MSFSLayoutGenerator to rebuild `layout.json`.
- Provides a German/English user interface.
- Keeps source files unchanged and writes results to a separate destination folder.
- Does not deliberately override material channels such as Roughness, Metallic, Ambient Occlusion, or alpha.
- Textures within the configured size limit are copied byte-for-byte; oversized textures still use the standard resize/re-encode pipeline, which can cause pixel-level differences.

## Requirements

- Windows 10/11.
- Python 3.10 or newer (check the exact requirements in the selected source snapshot).
- Python dependency: Pillow (`python -m pip install -r requirements.txt`).
- Microsoft DirectXTex `texconv.exe` for the DirectXTex/DDS/BC7 workflow.
- Khronos KTX-Software `ktx.exe` for supported KTX2 operations.
- MSFSLayoutGenerator is optional, but the package `layout.json` must be regenerated after the files are modified. The application can invoke the tool when configured.

External tools are **not bundled** in this repository. Download them from their official project pages and review their licenses and distribution terms:

- [Microsoft DirectXTex](https://github.com/microsoft/DirectXTex)
- [KhronosGroup KTX-Software](https://github.com/KhronosGroup/KTX-Software)
- [MSFSLayoutGenerator](https://github.com/HughesMDflyer4/MSFSLayoutGenerator)

## Run

1. Install Python.
2. Install the dependency listed in `requirements.txt`:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Download the required external tools and configure their executable paths in the application.
4. Run `Starten.bat`.

Read [README_EN.md](README_EN.md) or [README_DE.md](README_DE.md) for project information. The full user manuals and BC7/KTX2 notes are also included as `README_EN.txt`, `README_DE.txt`, `BC7_KTX2_NOTE_EN.txt`, and `BC7_KTX2_HINWEIS.txt` where present in the latest snapshot.

## Important notes

- Always choose a separate destination folder. Do not convert directly inside the source package.
- Rebuild `layout.json` after changing package files and before testing the output package in MSFS.
- The v1.6 snapshot removes copied `.ktx2p` files from the destination package after successful KTX2 conversion, according to the supplied implementation. The source package is not modified. Verify the output package in MSFS.
- Reduced KTX2 payload size is an estimate, not a guarantee of the exact VRAM reduction seen in the simulator. Runtime allocation, streaming, LOD selection, caching, and other aircraft resources affect measured VRAM. Use the MSFS DevMode SimObject Statistics Profiler for controlled comparisons.
- Back up and test the output before using it in a live simulator setup.

## Development history

See [CHANGELOG.md](CHANGELOG.md) and [HISTORY_RECONSTRUCTION.md](HISTORY_RECONSTRUCTION.md). Annotated Git tags are created for v1.0 (inferred earliest snapshot), v1.3, v1.4, v1.5, and v1.6. The archive labelled `MSFS4K_Converter_v2.zip` is included as an untagged intermediate KTX2-support commit because its exact semantic version could not be established from the archive contents. Some intermediate versions may still be missing.

The original ZIP snapshots are included in the GitHub setup bundle under `history-archives/`, but are not copied into the generated Git repository.

## License

Copyright (C) 2026 p0lfilt3r.

This project is licensed under the **GNU General Public License version 3.0 only (GPL-3.0-only)**. You may use, study, modify, and redistribute this software under the terms of that license. **Commercial use is permitted**; the GPL does not impose a non-commercial restriction. Distribution of the program or modified versions must comply with the GPL's applicable source-code, notice, and licensing requirements.

See [LICENSE](LICENSE) for the full license text. This license applies to this project's code; external tools retain their own separate licenses and terms.
