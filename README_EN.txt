MSFS 2024 – Livery 4K Converter 1.7 (Batch Processing)
=================================================

LANGUAGE SELECTION (NEW IN VERSION 1.5)
---------------------------------------
- Switch between “Deutsch” and “English” using the selector at the top right of the window.
- The selection applies to window labels, settings, dialogs, status messages and new log entries.
- The selected language is saved automatically and restored on the next launch.
- Existing log entries remain in the language in which they were originally written.

WHAT'S NEW IN VERSION 1.7
-------------------------
- The application chooses its initial window size based on the available display area.
- If the display is too small, a vertical scrollbar appears on the right so the bottom action buttons remain reachable.
- Selecting a source folder automatically fills the destination with the same path and an appended _4K suffix.
- A missing destination folder is created automatically when conversion starts.
- New batch mode: nested MSFS livery package folders are detected recursively and converted one by one.
- Each package is written to a sibling output folder whose name is the source folder name plus _4K.
- Existing _4K output folders are cleared completely and rebuilt before a batch run.
- Folders whose names end in _4K are never treated as source liveries.

WHAT'S NEW IN VERSION 1.6
-------------------------
- The application interface is bilingual (German/English).
- After at least one KTX2 texture is successfully modified, all copied .ktx2p files are removed from the DESTINATION package. Source files remain untouched.
- The language selector is at the top right and the selected language is remembered.
- All features from version 1.4 are retained.
- The destination folder is now created as a complete copy of the source folder.
- ALL files are copied: manifest.json, layout.json, CFG/JSON/XML files, thumbnails,
  documents, other files, and all textures.
- Textures that are already 4K or smaller are left unchanged.
- Only supported textures larger than the target size are resized in the destination.
- The folder structure and filenames are preserved.
- Optionally, MSFSLayoutGenerator.exe can be run automatically after conversion to
  update layout.json and, if present, total_package_size in manifest.json.
- Source files are never modified.

BATCH PROCESSING
----------------
- Select the parent folder that contains multiple livery packages.
- Enable “Batch processing” and start conversion.
- The application searches recursively for MSFS package roots (folders with SimObjects/Airplanes, or with SimObjects plus manifest.json/layout.json).
- Each detected package is copied and processed into a sibling folder named after the source folder with _4K appended.
- Existing _4K destination folders are completely cleared after a confirmation prompt. Source packages are never modified.
- Existing folders ending in _4K are skipped during discovery and are treated only as output folders.
- Parent categories and nested folder structures are retained; each _4K output is placed next to its source livery.

WHAT THE PROGRAM DOES
---------------------
- Scans a selected livery/package folder, including all subfolders.
- Creates a complete file copy in the destination folder.
- Resizes only images whose width OR height exceeds the configured maximum dimension.
- Preserves the aspect ratio when resizing.
- Rebuilds mipmaps for DDS files.
- For supported KTX2 files, scales the texture, re-encodes it, and rebuilds the mip chain.
- Native BC7-KTX2 files (VK_FORMAT_BC7_UNORM_BLOCK and VK_FORMAT_BC7_SRGB_BLOCK) are
  resized through DirectXTex/texconv and packaged back into KTX2.
- BC7 re-encoding can use DirectCompute on an NVIDIA GPU; CPU processing can also be
  selected in the application.
- For the BC7-KTX2 workflow, the KTX2 DFD and Key/Value metadata blocks are preserved,
  including ASOBO keys such as ASOBO_flags and ASOBOtexversion.

REQUIREMENTS (WINDOWS 10/11)
---------------------------
1. Install Python 3.9 or newer, if it is not already installed:
   https://www.python.org/downloads/windows/
   During installation, enable "Add Python to PATH".

2. Install Microsoft DirectXTex / texconv (for DDS, standard image files, and BC7-KTX2):
   Open PowerShell or Command Prompt and run:

   winget install Microsoft.DirectXTex.Texconv

   Documentation:
   https://github.com/microsoft/DirectXTex/wiki/texconv

3. Install Khronos KTX-Software (for KTX2 files):
   Download and extract the Windows version from:
   https://github.com/KhronosGroup/KTX-Software/releases

   In the application, select "ktx.exe" from the "bin" folder.

4. Install Pillow:
   python -m pip install -r requirements.txt

5. MSFS Layout Generator (recommended for ready-to-use MSFS package folders):
   Download a release:
   https://github.com/HughesMDflyer4/MSFSLayoutGenerator/releases/latest

   Save "MSFSLayoutGenerator.exe" in a permanent location and select it in the
   converter under "Layout Tool". It does not need to be copied into the program folder.

STARTING THE PROGRAM
--------------------
Double-click "Starten.bat".

HOW TO USE
----------
1. Select the ROOT FOLDER of the complete livery/package as the source folder.
   This is usually the folder containing manifest.json and layout.json.
   Do not select only the texture subfolder.
2. Select a separate destination folder. The suggested folder name ends in "_4K".
3. Select texconv.exe if it was not detected automatically.
4. Select ktx.exe if KTX2 files are present and it was not detected automatically.
5. Select MSFSLayoutGenerator.exe in the "Layout Tool" field.
6. Leave the maximum dimension at 4096, unless you want a different target size.
7. For BC7, leave GPU acceleration enabled. DirectCompute adapter 0 is used by default.
   On hybrid laptops, try adapter 1 if the NVIDIA GPU is not selected.
8. Click "Start Conversion".

The converter first copies all files to the destination folder. It then replaces only
supported textures that exceed the target size. If a texture conversion fails, the
original file that was copied to the destination is kept.

IMPORTANT: THE DESTINATION FOLDER
---------------------------------
- For best results, use a new, empty destination folder.
- If the destination folder already contains files, files with matching relative paths
  are overwritten. Extra old files that are no longer present in the source are NOT
  deleted automatically, as a safety measure.
- The source folder is always left unchanged.
- Destination-only exception: after a successful KTX2 edit, .ktx2p files are removed
  because they may contain stale packed texture data. They remain in the source folder.

MSFS LAYOUT.JSON – DO I NEED MSFSLayoutGenerator.exe?
----------------------------------------------------
If the source folder contains layout.json and textures are resized, layout.json should
be updated after conversion. This file lists package files together with their sizes
and modification times. After a texture has changed, those entries no longer match the
files on disk.

If "MSFSLayoutGenerator.exe" is selected in the converter, it is automatically run
after copying and conversion, using the layout.json file in the destination folder.
The tool rebuilds the file list and also updates total_package_size in manifest.json,
provided that this property exists in the manifest.

If no Layout Tool is configured, all files are still copied and textures are still
converted. However, the converter displays a reminder that layout.json still needs to
be updated. You can then drag the DESTINATION layout.json onto MSFSLayoutGenerator.exe,
or regenerate it through the MSFS SDK/package workflow.

MSFSLayoutGenerator.exe is therefore not the texture conversion engine. It is used to
update the package file list (or can be replaced by an equivalent SDK/layout workflow).
For a Community package folder that is intended to be used directly, we recommend
configuring this tool.

Examples of dimension scaling:
  8192 × 8192  ->  4096 × 4096
  8192 × 4096  ->  4096 × 2048
  8192 × 2048  ->  4096 × 1024
  4096 × 4096  ->  unchanged

KTX2 SUPPORT AND LIMITATIONS
----------------------------
Supported standard 2D KTX2 textures include the following formats:
- BC7 UNORM and BC7 sRGB.
- UASTC / ETC1S (BasisLZ), provided they can be read by the installed KTX-Software.
- ASTC LDR textures.
- 8-bit RGB/RGBA UNORM and sRGB textures.

BC7 re-encoding uses Microsoft DirectXTex/texconv. When the GPU option is enabled,
the program passes the DirectCompute adapter index through texconv's -gpu option.
The adapter ID is the DirectX/DirectCompute device index and is not necessarily the
same as the CUDA device index.

Some MSFS 2024 files are not standard, publicly readable KTX2 files. Files with the
supercompression value 65536 are detected, copied unchanged, and skipped during
conversion. Such files may need to be extracted using the MSFS Livery Toolkit and then
rebuilt with the MSFS SDK:
https://github.com/theflaknine/MSFS-Livery-Toolkit/releases/latest

IMPORTANT – KTX2P AND VRAM REDUCTION
-------------------------------------
MSFS 2024 may continue using old packed texture data from .ktx2p files even after
individual .ktx2 files have been resized. Microsoft documents this behavior in the SDK
and recommends removing KTX2P files after directly modifying KTX2 textures.

Therefore, after at least one KTX2 texture has been resized successfully, version 1.6
automatically removes all .ktx2p files from the DESTINATION folder. Original files in
the SOURCE folder are never deleted. MSFS then falls back to the individual KTX2 files.
If MSFSLayoutGenerator.exe is configured, layout.json is rebuilt afterwards so the
removed KTX2P files are also removed from the package file list.

If no KTX2 texture was successfully modified, KTX2P files are not removed. Use a fresh,
empty destination folder for each conversion whenever possible.

MSFS NOTES
----------
- Whenever possible, select the complete package root as the source folder
  (the folder containing manifest.json/layout.json).
- Test the generated destination folder as a separate package and keep the original
  as a backup.
- Changes to already compiled/protected add-ons may require rebuilding the package
  with the MSFS 2024 SDK.
- Make sure the add-on is explicitly compatible with MSFS 2024.

TROUBLESHOOTING
---------------
"texconv.exe not found":
  winget install Microsoft.DirectXTex.Texconv

"ktx.exe not found":
  Install Khronos KTX-Software and select ktx.exe from its bin folder.

"layout.json not updated":
  Download MSFSLayoutGenerator.exe and select it in the application under "Layout Tool".
  Alternatively, drag the layout.json file from the DESTINATION folder onto the EXE.

"Pillow missing":
  python -m pip install -r requirements.txt

License note:
This utility uses Microsoft DirectXTex/texconv, Khronos KTX-Software, and optionally
MSFSLayoutGenerator as separate tools. These third-party tools are not included;
their respective license terms apply separately.

GPU NOTE
--------
- GPU acceleration applies to BC7 re-encoding in texconv.
- Enabled: texconv is called with -gpu <adapter-index>.
- Disabled: texconv is called with -nogpu for CPU mode.
- If errors occur, first try adapter 0/1 or enable CPU mode.
