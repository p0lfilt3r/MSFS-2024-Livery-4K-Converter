MSFS 2024 – Livery 4K Converter v1.8
User Guide (English)

Purpose
The application creates a separate, lower-resolution copy of MSFS 2024 livery packages. Source files are not modified.

Requirements
- Windows 10/11
- Python 3.10 or newer
- Pillow (install with: python -m pip install -r requirements.txt)
- Microsoft DirectXTex (texconv.exe) for supported DDS/BC7 operations
- Khronos KTX-Software (ktx.exe) for supported KTX2 operations
- Optional: MSFSLayoutGenerator to rebuild layout.json

Getting started
1. Install the required software and configure its executable paths in the converter.
2. Run Starten.bat.
3. Select German or English.
4. Select the source livery folder. A sibling destination path with the _4K suffix is suggested automatically.
5. Enable batch processing to recursively process nested livery packages when needed.
6. Start conversion. Missing destinations are created; existing batch destinations are rebuilt after confirmation.

Surface and material properties
There is no option to change matte/gloss or metalness. The converter does not deliberately override material channels such as Roughness, Metallic, Ambient Occlusion or alpha. Textures within the configured size limit are copied byte-for-byte. Oversized textures still go through the normal resize/re-encode pipeline and may have technical pixel-level differences.

Important notes
- Never convert directly inside the source package; always use a separate destination.
- Rebuild layout.json after package files are changed when required by the aircraft package.
- Test the result in MSFS 2024 before regular use.
- External tools are not bundled and remain subject to their own licenses.
