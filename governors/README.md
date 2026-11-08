# Governor stance evidence

Start with [GOVERNOR-PUBLIC-TAKES.md](GOVERNOR-PUBLIC-TAKES.md). It covers all 50 states, separating projected incoming governors from actual holdovers and unresolved races. [CSV](governor-summary.csv) and [JSONL](governor-summary.jsonl) versions support other instances and analysis.

**The evidence cutoff is November 4, 2026, America/New_York.** This is a publication of existing independently reviewed research, not a fresh policy or election update. Certification was not verified. Alaska and Kansas retain unresolved incoming identities; candidates and outgoing governors must not be substituted for winners. Hawaii's reviewed public-IT evidence does not establish a private hyperscale stance. Unknown is not neutral.

## Which raw evidence matters most

1. **The governor's own dated words:** official statements, authored plans, veto messages, interview answers and debate transcripts. They establish a public position. A host, opponent, spokesperson or journalist is a different speaker; those distinctions remain in the reviewed claims.
2. **The actual legal instrument:** signed executive order, enacted statutory text, veto and official disposition. Read operative sections, thresholds, exemptions, effective dates and the responsible agency. A press release describing an order is weaker than the accessible order itself.
3. **Implementation records:** adopted utility tariffs, commission orders, agency guidelines, actual permit decisions and executed agreements. They distinguish a policy announcement from a rule or action in force. A governor's request to an independent regulator is not the regulator's decision.
4. **Earlier contrary actions:** incentive signatures, earlier project endorsements, personal legislative votes and corrected votes. These keep a later pause pledge from erasing a mixed record. Predecessor actions and a candidate's prior office remain separately attributed.
5. **Dated identity/call evidence:** this determines whose position belongs to the incoming roster. It does not prove certification, inauguration or implementation of campaign promises.

Construction bans, incentive-application pauses, particular environmental-permit holds, state-land restrictions and local moratoria have different scopes. General AI regulation is not a proxy for construction policy. Public positions do not establish delayed MW or approval probabilities.

## Evidence files

- [source-index.jsonl](source-index.jsonl): governor-specific source receipts with URLs, dates, locators, access qualifications and supporting claim IDs. Receipts are metadata, not copies of the source bodies. Source IDs are scoped by state, ID and URL.
- [evidence/governor-evidence.tar.gz](evidence/governor-evidence.tar.gz): 584 previously reviewed governor claims, 32 held clauses, all 50 governor coverage/checklist entries, original researcher records/source indexes/handoffs/search logs, independent review decisions and selected exact legal-document capture segments.
- [evidence/manifest.json](evidence/manifest.json): per-member SHA256, original paths, the original capture-file inventory and precise provenance for 161 preserved legal-document segments. The inventory includes captures whose full bodies were not uploaded.
- [curated-takes.json](curated-takes.json): the human-written summaries and explicit supporting claim IDs.
- [build_governor_bundle.py](build_governor_bundle.py): reproducible extraction and hash/state/claim validation. Requires the original research workspace; reading the published bundle does not.

Original researcher packets are **candidate submissions**, not independent approvals. Use `reviewed/governor-claims.jsonl` together with verdicts and holds. Some original dossiers predate later review corrections; the reviewed claims control this summary. Legal captures also include context such as introduced or unsuccessful bills: their presence does not establish enactment or the governor's personal endorsement.

The legal-document segments are unchanged text substrings from saved tool responses. Their manifest records the original tool file hash, content-block hash, character range and segment hash. They are historical captured text, **not complete original PDFs, new network readbacks or inspected signature images**. News/interview bodies are represented by reviewed paraphrases and source locators rather than uploaded full articles. Full original captures remain in the source workspace for the planned external archive.

## Read from another instance

Clone `https://github.com/RonaldQiao/blue-wave-dc`, then:

```sh
mkdir governor-evidence
tar -xzf governors/evidence/governor-evidence.tar.gz -C governor-evidence
```

The archive expands below that directory. Verify SHA256 against `governors/evidence/manifest.json` before relying on a member. Absolute `/workspace/...` fields describe the historical source environment; use archive member paths on a different machine. Do not restore old leases as proof that workers are running, overwrite a newer database or restart the completed political research automation.
