# Reconstructed Git history

The history is reconstructed from seven ZIP snapshots supplied by the project owner, ordered from the oldest source snapshot to the latest supplied release.

1. **Initial converter snapshot** – `MSFS_2024_Livery_4K_Converter.zip`; no KTX2 processing. The import script creates an inferred `v1.0` tag because this is the earliest supplied snapshot.
2. **Intermediate KTX2-support snapshot** – `MSFS4K_Converter_v2.zip`; adds early KTX2 support. The archive name contains `v2`, but the source does not expose a reliable semantic version. It is included as an untagged commit.
3. **v1.3 – NVIDIA / BC7** – adds BC7 processing and optional DirectCompute adapter acceleration.
4. **v1.4 – Full package copy** – copies the complete package and adds optional layout regeneration.
5. **v1.4 documentation update** – separate documentation-only commit adding English user and BC7/KTX2 notes.
6. **v1.5 – Bilingual interface** – adds German/English UI selection.
7. **v1.6 – KTX2P handling** – adds the KTX2P destination-package behavior.

The version sequence is not complete: intermediate snapshots between the supplied early KTX2 archive and v1.3 may be missing. The `v1.0` tag is an explicit inference based on the earliest supplied archive, not a recovered original tag.

ZIP files do not contain original Git objects, commit messages, or reliable commit timestamps. The import script creates new commits in chronological order using the Git identity configured on the user's computer and the date/time at import.

The snapshots are used as commit contents. Temporary Python cache files (`__pycache__`, `.pyc`) are excluded. The original ZIP archives remain in the setup bundle under `history-archives/` and are not copied into the generated repository.

## Timestamp correction

At the user's request, ZIP entry timestamps on 2026-10-30 were shifted to 2026-10-31 with clock times preserved. Entries on 2026-11-01 were left unchanged. The reconstructed Git commits use ZIP-derived representative times (latest non-cache file in each snapshot), interpreted as Europe/Berlin UTC+01:00. These are reconstructed dates, not original Git commit dates. See `TIMESTAMP_POLICY.md` and `SOURCE_ARCHIVES_INDEX.md`.
