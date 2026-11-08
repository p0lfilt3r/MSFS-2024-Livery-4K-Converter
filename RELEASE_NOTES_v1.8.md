# MSFS 2024 Livery 4K Converter v1.8

## Original material properties are always preserved

- Removed the surface-finish checkbox and both roughness/metalness sliders.
- Removed code paths that deliberately override COMP/ORM material channels.
- Textures that do not exceed the configured dimension limit are copied byte-for-byte.
- Oversized textures continue through the normal resize/re-encode pipeline. Resampling, mipmap generation and compression can cause technical pixel-level differences, but no material channel is deliberately assigned a new value.
- Single-package and recursive batch processing use the same behavior.

## Retained features

- Recursive batch processing of nested livery packages.
- Sibling *_4K output folders, with existing batch destinations rebuilt after confirmation.
- Responsive window and right-side scrollbar.
- DDS/KTX2 processing, BC7 support, KTX2P handling, bilingual interface and layout.json update workflow.
