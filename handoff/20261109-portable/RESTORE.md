# Portable snapshot — November 9, 2026

The archive extracts a `datacenter-construction/` folder. Choose an EMPTY destination and verify hashes before use. The original /workspace paths in historical reports and the queue belong to the producing instance; they do not automatically exist in a new instance. For analysis, resolve reports and exports relative to this extracted folder. `exports/latest.json` retains the original provenance path; use its version as the local exports subdirectory name. Do not silently rewrite the historical pointer or SQLite absolute paths.

Hourly automation is OFF by explicit user request. A restored automation.json does not control the native scheduler of a different instance. Do not create/re-enable a timer. Database leases/checkpoints are historical, not runtime activity. This snapshot includes reviewed outputs, instructions, reports and a coherent historical queue backup. It omits full raw worker evidence, CAS/archive objects, independent-review history and dashboard source. Do not use it alone to claim evidence closure or dispatch/resume workers. Obtain omitted dependencies and reconcile live ownership before any separately authorized resumption.

Existing governor stance publication is in the repository's governors/ folder, evidence cutoff November4. GitHub readback verified its guide November9; earlier HANDOFF.md's uncertainty about publication is superseded by this note. Governors and their original public evidence remain unchanged.

## Retrieve and restore

Clone or safely refresh `https://github.com/RonaldQiao/blue-wave-dc`. From the repository root run:

```bash
python handoff/20261109-portable/restore.py /workspace/restored-dc-research
```

The destination must be absent or empty. The helper checks the archive hash and every member hash before extraction. Read `datacenter-construction/PORTABLE-RESTORE-NOTES.md` in that destination. Do not overwrite an existing research workspace or treat historical leases as running agents.

The newer construction report is inside `datacenter-construction/reports/20261108T2053/`; the canonical reviewed outputs are inside `datacenter-construction/exports/2026-11-08T212951175852+0000-c04506ac/`. These snapshot paths are relative to the chosen restore destination. The copied queue and provenance pointer retain original absolute paths; analysis should resolve files relative to the snapshot. Do not rewrite immutable provenance silently.
