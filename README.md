# Blue-wave data-center research

Start with the newer [HANDOFF.md](HANDOFF.md) for the Cleanview report and cross-instance access. The hourly timer is OFF. LATEST-HANDOFF.json still points to the older November7 inventory archive; no newer full database snapshot has been published.

## Governor-specific public positions and evidence

See [the 50-state governor summary](governors/GOVERNOR-PUBLIC-TAKES.md) and [the governor evidence guide](governors/README.md). The guide includes the original legal-capture bundle, source locators and review provenance. This governor slice is dated to the November 4, 2026 evidence cutoff; it is not a fresh election or policy update.

Portable handoff for sharing between instances through https://github.com/RonaldQiao/blue-wave-dc. Public publication was explicitly authorized by the user. See LATEST-HANDOFF.json for the hash-verified reviewed-output archive and coherent construction queue snapshot.

## Original working files

- Construction: /workspace/datacenter-construction
- Completed political stance research: /workspace/datacenter-political-risk
- Existing private dashboard source: /workspace/sites/agent-monitor

These paths belong to this environment, not automatically to other instances. A Git push or external shared-storage upload is required. Symlinks alone do not share evidence.

## What this handoff contains

Reviewed construction CSV/JSONL, coverage/manifest/source-ID closure; final political records, holds, context, incoming roster, audit/checklists; operating instructions; a coherent compressed construction queue snapshot. Raw worker evidence, full review history, archive/CAS objects and dashboard source remain local, pending external storage transfer. This is a partial handoff, not an independent full backup.

## Access from another instance

Clone this repository, read LATEST-HANDOFF.json and the corresponding manifest, then extract reviewed-handoff.tar.gz into an empty research directory. This is a fixed snapshot; later local research is not automatically synced here.

## Resume safely

Verify archive and per-file SHA256 against the manifest before extracting into an empty destination. Restore the queue snapshot only when no newer live database exists. Historical leases/checkpoints do not establish running workers. Inspect actual collaboration status, acquire the transactional dispatcher lock and reconcile task ownership before dispatch. All submitted addenda require independent review and successful canonical export before acceptance. Preserve the completed political phase and disabled automation.

Construction coverage is preliminary, not exhaustive; whole-facility capacity is not unfinished capacity. The dashboard is a dated saved snapshot while authenticated continuous uploads return403.
