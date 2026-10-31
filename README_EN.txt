MSFS 2024 – Livery 4K Converter 1.4 (Full Package)
=================================================

WHAT'S NEW IN VERSION 1.4
-------------------------
- The destination folder is now created as a complete copy of the source folder.
- ALL files are copied: manifest.json, layout.json, CFG/JSON/XML files, thumbnails,
  documents, other files, and all textures.
- Textures that are already 4K or smaller are left unchanged.
- Only supported textures larger than the target size are resized in the destination.
- The folder structure and filenames are preserved.
- Optionally, MSFSLayoutGenerator.exe can be run automatically after conversion to
  update layout.json and, if present, total_package_size in manifest.json.
- Source files are never modified.

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

KTX2P files are packed streaming files, not individual textures. They are copied
unchanged but are not processed as image textures.

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
