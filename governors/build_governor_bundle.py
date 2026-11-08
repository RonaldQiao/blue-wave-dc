"""Package the frozen, reviewed governor slice; never alter the source dataset.

Run with an explicit original workspace. Outputs are a dated handoff, not fresh
election or policy verification. The legal-capture excerpts preserve exact
substrings of saved tool responses; they are not original PDFs or full articles.
"""
import argparse
import collections
import csv
import datetime
import gzip
import hashlib
import io
import json
import pathlib
import re
import tarfile
import urllib.parse

HERE = pathlib.Path(__file__).resolve().parent
SHA = lambda b: hashlib.sha256(b).hexdigest()


def rows(path):
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


def write_rows(path, data):
    path.write_text(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in data))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', required=True, type=pathlib.Path)
    args = parser.parse_args()
    root = args.source.resolve()
    export = root / 'data/reviewed-consolidated/20261106T052329Z'
    audit = root / 'reviews/final-review6-audits/20261106T052333Z'
    claims = [r for r in rows(export / 'records.jsonl') if r.get('office') == 'governor']
    seats = [r for r in rows(audit / 'seat-checklist.jsonl') if r['office'] == 'governor']
    coverage = rows(export / 'governor-coverage.jsonl')
    takes = json.loads((HERE / 'curated-takes.json').read_text())
    assert len(seats) == len(coverage) == len(takes) == 50
    assert len({r['stable_claim_id'] for r in claims}) == len(claims)
    by_id = {r['record_id']: r for r in claims}
    by_seat = {r['canonical_seat_id']: r for r in seats}
    manifest = {'created_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'evidence_cutoff': '2026-11-04 America/New_York',
                'reviewed_export': str(export.relative_to(root)),
                'reviewed_export_manifest_sha256': SHA((export / 'manifest.json').read_bytes()),
                'kind': 'Frozen governor evidence handoff; no fresh web verification',
                'files': [], 'raw_capture_inventory': [], 'legal_capture_segments': []}
    for state, (_, _, ids) in takes.items():
        for rid in ids:
            assert rid in by_id, (state, rid)
            assert by_id[rid]['state'] == state
            assert by_id[rid]['eligible_for_stance_score'] is True
            assert by_id[rid]['comparison_role'] != 'outgoing_actor'

    summaries = []
    for state in sorted(takes):
        label, take, ids = takes[state]
        seat = by_seat['US-GOV-' + state]
        incoming = seat.get('reviewed_incoming_actor')
        own = [r for r in claims if r['state'] == state and r['actor'] == incoming
               and r.get('comparison_role') != 'outgoing_actor']
        holdover = any(r.get('comparison_role') == 'actual_holdover_actor' for r in own)
        status = ('unresolved; candidates kept separate' if incoming is None else
                  'actual holdover; not a 2026 election winner' if holdover else
                  'projected incoming/returning; certification not verified')
        evidence = []
        seen = set()
        for rid in ids:
            r = by_id[rid]
            for source in r.get('sources', []):
                url = source.get('url') or source.get('original_url') or source.get('source_url')
                if not url or url in seen:
                    continue
                seen.add(url)
                evidence.append({'claim_id': rid, 'stable_claim_id': r['stable_claim_id'],
                    'claim_date': r.get('date'), 'source_id': source.get('source_id'),
                    'url': url, 'title': source.get('title') or source.get('publisher') or url,
                    'publication_date': source.get('normalized_publication_date') or source.get('publication_date') or source.get('date'),
                    'locator': source.get('document_locator') or source.get('pinpoint_locator') or source.get('locator') or source.get('pinpoint'),
                    'source_type': source.get('source_type') or source.get('evidence_role'),
                    'limitations': source.get('access_limitations') or source.get('notes')})
        summaries.append({'state': state, 'seat_id': seat['canonical_seat_id'],
                          'governor_or_projected_incoming': incoming,
                          'roster_status': status, 'reviewed_election_status': seat.get('reviewed_election_status'),
                          'public_take_label': label, 'public_take': take,
                          'claim_ids': ids, 'key_sources': evidence,
                          'general_ai_policy': 'Separate reviewed clauses retained; not used to infer physical-buildout stance.',
                          'as_of': manifest['evidence_cutoff']})
    write_rows(HERE / 'governor-summary.jsonl', summaries)
    with (HERE / 'governor-summary.csv').open('w', newline='') as f:
        fields = ['state', 'seat_id', 'governor_or_projected_incoming', 'roster_status',
                  'public_take_label', 'public_take', 'claim_ids', 'key_source_urls', 'as_of']
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for r in summaries:
            writer.writerow({**{k: r.get(k) for k in fields if k not in ['claim_ids', 'key_source_urls']},
                             'claim_ids': '; '.join(r['claim_ids']),
                             'key_source_urls': '; '.join(s['url'] for s in r['key_sources'])})

    md = ['# Governors: public positions on data-center buildout', '',
          '**Evidence cutoff: November 4, 2026, America/New_York.** Prepared from the independently reviewed snapshot; not a fresh November 8 update. A projected win does not establish certification or start a new term; returning incumbents may already hold office. Holdovers are distinct. Alaska and Kansas have no resolved incoming identity in this snapshot. Unknown is not neutral.', '',
          'A construction moratorium, a pause in tax applications, a hold on particular permits, and restrictions on state land are different actions. Proposals are not enacted rules. General AI policy is retained separately in the evidence archive and does not determine the physical-buildout label. These summaries do not predict delayed MW.', '',
          '## At a glance', '',
          '| State | Governor / projected incoming | Status at cutoff | Public take |',
          '|---|---|---|---|']
    for r in summaries:
        name = r['governor_or_projected_incoming'] or 'Unresolved'
        md.append(f"| [{r['state']}](#{r['state'].lower()}) | {name} | {r['roster_status']} | {r['public_take_label']} |")
    for r in summaries:
        md += ['', f"<a id=\"{r['state'].lower()}\"></a>",
               f"## {r['state']} — {r['governor_or_projected_incoming'] or 'Incoming identity unresolved'}", '',
               f"**{r['public_take_label']}.** {r['public_take']}", '',
               f"Roster: {r['roster_status']}. Exact reviewed status: `{r['reviewed_election_status'] or 'no 2026 call assigned'}`.", '']
        if r['key_sources']:
            md += ['Key evidence:', '']
            for s in r['key_sources'][:7]:
                title = str(s['title']).replace('[', '').replace(']', '')
                locator = s['locator'] or 'see exact source metadata in summary JSONL'
                md.append(f"- [{title}]({s['url']}) — source date {s['publication_date'] or 'unknown'}; {locator}; claim `{s['claim_id']}`.")
        else:
            md += ['The unresolved-candidate research and review dispositions are preserved in the evidence archive; no winner is inferred from a leader or self-declaration.']
        md += ['', 'All selected claim IDs: ' + (', '.join('`' + x + '`' for x in r['claim_ids']) or 'none assigned to an incoming governor') + '.']
    (HERE / 'GOVERNOR-PUBLIC-TAKES.md').write_text('\n'.join(md) + '\n')

    # Own analytical records and receipts remain inspectable without full news bodies.
    source_rows = {}
    for r in claims:
        for source in r.get('sources', []):
            url = source.get('url') or source.get('original_url') or source.get('source_url')
            key = (r['state'], source.get('source_id'), url)
            if key not in source_rows:
                safe = {k: v for k, v in source.items()
                        if k not in ['exact_excerpt', 'exact_quote', 'excerpt', 'quote', 'text', 'body', 'content']}
                source_rows[key] = {'state': r['state'], 'source': safe, 'claim_ids': []}
            source_rows[key]['claim_ids'].append(r['record_id'])
    write_rows(HERE / 'source-index.jsonl', list(source_rows.values()))
    archive_path = HERE / 'evidence/governor-evidence.tar.gz'
    added = set()
    with tarfile.open(archive_path, 'w:gz') as archive:
        def add_bytes(b, name, original=None):
            if name in added:
                return
            added.add(name)
            info = tarfile.TarInfo(name)
            info.size = len(b)
            archive.addfile(info, io.BytesIO(b))
            manifest['files'].append({'path': name, 'bytes': len(b), 'sha256': SHA(b), 'original_path': original})

        def add_file(f):
            add_bytes(f.read_bytes(), str(f.relative_to(root)), str(f))

        add_bytes(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in claims).encode(),
                  'reviewed/governor-claims.jsonl', str(export / 'records.jsonl') + ' [governor slice]')
        held = [r for r in rows(export / 'holds.jsonl') if 'US-GOV-' in str(r.get('dossier', ''))]
        add_bytes(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in held).encode(), 'reviewed/governor-holds.jsonl')
        add_bytes(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in coverage).encode(), 'reviewed/governor-coverage.jsonl')
        add_bytes(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in seats).encode(), 'reviewed/governor-seat-checklist.jsonl')
        add_file(root / 'FINAL-COVERAGE.md')
        packet_dirs = set()
        for seat in seats:
            d = pathlib.Path(seat['queue_output'])
            d = d if d.is_absolute() else root / d
            packet_dirs.add(d)
        for r in claims:
            packet_dirs.add(pathlib.Path(r['original_candidate_path']).parent)
        review_dirs = {pathlib.Path(r['verdict_sidecar']).parent for r in claims}
        for seat in seats:
            for batch in seat.get('selected_review_batches', []):
                review_dirs.add(root / 'reviews' / batch)
        for d in sorted(packet_dirs):
            for name in ['records.jsonl', 'sources.jsonl', 'handoff.md', 'search-log.jsonl']:
                if (d / name).is_file():
                    add_file(d / name)
        for d in sorted(review_dirs):
            for name in ['record-verdicts.jsonl', 'summary.json', 'README.md', 'intake-original-hashes.json', 'input-audit.json']:
                if (d / name).is_file():
                    add_file(d / name)

        # Extract exact saved legal-document segments, excluding full copyrighted
        # news/interview bodies and search-result-only blocks. Context can include
        # introduced/failed bills: capture presence never establishes enactment.
        capture_files = set()
        for d in packet_dirs:
            capture_files.update(f for f in d.rglob('*.json') if '/raw/' in str(f))
        for d in review_dirs:
            capture_files.update(d.glob('raw*.json'))
        segment_seen = set()
        for f in sorted(capture_files):
            b = f.read_bytes()
            manifest['raw_capture_inventory'].append({'original_path': str(f.relative_to(root)), 'bytes': len(b),
                                                     'sha256': SHA(b), 'full_capture_uploaded': False})
            try:
                captured = json.loads(b)
            except ValueError:
                continue
            if not isinstance(captured, dict):
                continue
            for bi, block in enumerate(captured.get('content', [])):
                if not isinstance(block, dict) or block.get('type') != 'text':
                    continue
                text = block['text']
                for part in re.split(r'\n-{20,}\n', text):
                    first = part.splitlines()[0] if part.splitlines() else ''
                    urls = re.findall(r'https?://[^\s<>\)]+', first)
                    if not urls:
                        continue
                    url = urls[-1]
                    host = urllib.parse.urlsplit(url).hostname or ''
                    legal = bool(re.search(r'executive.order|/eo\d|/laws/|/bills/|/billtext|/legislation/|/statutes/|/sessionlaw|/chapters/|/BillDetail|/lawfiles/', url, re.I))
                    legal = legal or ('executive order' in first.lower() and host.endswith('.gov'))
                    opened = re.search(r'\bL\d+(?:@P\d+)?:', part)
                    if not (legal and host.endswith('.gov') and opened):
                        continue
                    if re.search(r'(^Error|403 Forbidden|404 Not Found|Internal Error|Failed to fetch)', first, re.I):
                        continue
                    digest = SHA(part.encode())
                    if digest in segment_seen:
                        continue
                    segment_seen.add(digest)
                    name = 'legal-capture-segments/' + digest[:20] + '.txt'
                    add_bytes(part.encode(), name, str(f.relative_to(root)))
                    manifest['legal_capture_segments'].append({'path': name, 'url': url,
                        'original_tool_file': str(f.relative_to(root)), 'original_file_sha256': SHA(b),
                        'content_block_index': bi, 'content_block_sha256': SHA(text.encode()),
                        'segment_character_start': text.find(part), 'segment_characters': len(part),
                        'segment_sha256': digest,
                        'scope': 'Exact substring of historical saved tool response, not a complete original document or fresh retrieval; bill/order status requires reviewed claim.'})

    manifest['archive_sha256'] = SHA(archive_path.read_bytes())
    manifest['archive_bytes'] = archive_path.stat().st_size
    manifest['coverage'] = {'states': len(seats), 'known_incoming_or_holdover_identities': sum(bool(r.get('reviewed_incoming_actor')) for r in seats),
                            'unresolved_states': [r['canonical_seat_id'] for r in seats if not r.get('reviewed_incoming_actor')],
                            'reviewed_claims': len(claims), 'held_clauses': len(held),
                            'source_receipts': len(source_rows), 'legal_capture_segments': len(segment_seen)}
    # Validate every published archive member and every curated claim/state join.
    with tarfile.open(archive_path, 'r:gz') as archive:
        assert len(archive.getmembers()) == len(manifest['files'])
        for entry in manifest['files']:
            assert SHA(archive.extractfile(entry['path']).read()) == entry['sha256']
    (HERE / 'evidence/manifest.json').write_text(json.dumps(manifest, indent=2))
    print(json.dumps({'validation': 'all archive hashes and 50 state/claim joins passed', **manifest['coverage'],
                      'archive_bytes': manifest['archive_bytes']}))


if __name__ == '__main__':
    main()
