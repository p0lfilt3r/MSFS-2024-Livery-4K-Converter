# Changelog

This history is reconstructed from the ZIP snapshots supplied by the project owner. The exact original Git commits and reliable creation timestamps are not available in ZIP archives. See `HISTORY_RECONSTRUCTION.md` for details.

## v1.8 – Original material preservation

- Removes the surface-finish checkbox and the roughness/metalness sliders.
- Removes deliberate COMP/ORM channel overrides.
- Copies textures below the configured dimension limit byte-for-byte.
- Oversized textures continue through the normal resize/re-encode pipeline; resampling, mipmap generation, and compression can cause technical pixel-level differences.
- Retains recursive batch processing, `_4K` output folders, responsive window, and right-side scrollbar.

## v1.7 – Batch processing and responsive window

- Adds recursive batch processing of nested livery packages.
- Automatically creates corresponding `_4K` destination folders.
- Rebuilds existing destination folders when processing starts.
- Excludes generated `_4K` folders from source discovery.
- Adjusts the application window to the available screen size.
- Adds a vertical scrollbar on the right for smaller displays.

## v1.6 – KTX2P handling
- Adds handling for copied `.ktx2p` files in the destination package after successful KTX2 conversion.
- Updates German and English documentation and technical notes.
- Retains the bilingual UI and previous package-copy and texture-conversion features.

## v1.5 – Bilingual interface
- Adds a German/English language selector in the application window.
- Persists the selected UI language between application starts.
- Translates application interface elements, dialogs, status text, and diagnostic messages.

## v1.4 – Full package copy
- Copies the complete livery/package folder, preserving directory structure and non-texture files.
- Resizes supported textures above the configured target size.
- Adds optional invocation of MSFSLayoutGenerator for `layout.json` regeneration.
- A later documentation-only snapshot adds English user and BC7/KTX2 documentation.

## v1.3 – NVIDIA / BC7
- Adds the BC7/KTX2 processing path based on DirectXTex.
- Adds selectable DirectCompute adapter acceleration where supported by the installed tool and GPU.

## Earlier snapshots
- **Initial converter (v1.0 tag inferred):** First supplied Windows GUI snapshot for resizing livery textures; it predates KTX2 support.
- **Intermediate KTX2 snapshot (archive named `MSFS4K_Converter_v2.zip`):** Adds early standard KTX2 processing. Its exact semantic version is not embedded in the source, so it is imported as an untagged commit rather than assigned a guessed release tag.
