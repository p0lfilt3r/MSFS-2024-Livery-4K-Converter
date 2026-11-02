# Timestamp policy for reconstructed Git history

The supplied ZIP snapshots contain file timestamps, but not original Git commit objects. The import script therefore reconstructs one commit timestamp per snapshot from the latest timestamp of a non-cache file in that archive.

At the user's request, all ZIP member timestamps dated 2026-10-30 were shifted to 2026-10-31, preserving clock time. ZIP entries dated 2026-11-01 were not changed. The corresponding reconstructed author and committer dates follow this adjusted date/time (Europe/Berlin, UTC+01:00).

The final project-overview documentation commit is created at the actual time the import script runs. Git does not preserve individual file modification times; only commits have dates.

This is a documented reconstruction, not a claim that these are recovered original Git commit timestamps.
