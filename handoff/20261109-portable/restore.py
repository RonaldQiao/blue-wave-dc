#!/usr/bin/env python3
"""Verify and restore the approved snapshot into an absent or empty directory. No automation starts."""
import hashlib,json,pathlib,sys,tarfile
base=pathlib.Path(__file__).resolve().parent
if len(sys.argv)!=2:raise SystemExit('Usage: python restore.py EMPTY_DESTINATION')
dest=pathlib.Path(sys.argv[1]).expanduser()
if dest.is_symlink():raise SystemExit('Refusing a symlink destination')
if dest.exists() and (not dest.is_dir() or any(dest.iterdir())):raise SystemExit('Destination must be absent or empty; refusing overwrite')
m=json.loads((base/'manifest.json').read_text());name=m['archive']['path']
if pathlib.PurePosixPath(name).name!=name:raise SystemExit('Invalid archive filename')
archive=base/name
if archive.stat().st_size!=m['archive']['bytes']:raise SystemExit('Archive byte count mismatch')
if hashlib.sha256(archive.read_bytes()).hexdigest()!=m['archive']['sha256']:raise SystemExit('Archive SHA-256 mismatch')
expected={x['path']:x for x in m['files']}
if len(expected)!=len(m['files']):raise SystemExit('Duplicate manifest member')
with tarfile.open(archive,'r:gz') as t:
 members=t.getmembers();seen=set()
 for member in members:
  path=pathlib.PurePosixPath(member.name)
  if path.is_absolute() or '..' in path.parts or not (member.isdir() or member.isfile()):raise SystemExit('Unsafe archive member: '+member.name)
  if member.isfile():
   if member.name in seen or member.name not in expected:raise SystemExit('Unexpected or duplicate file: '+member.name)
   seen.add(member.name);info=expected[member.name]
   if member.size!=info['bytes'] or hashlib.sha256(t.extractfile(member).read()).hexdigest()!=info['sha256']:raise SystemExit('Member verification failed: '+member.name)
 if seen!=set(expected):raise SystemExit('Archive missing manifest files')
 dest.mkdir(parents=True,exist_ok=True)
 t.extractall(dest,filter='data')
print(f'Verified and restored {len(seen)} files to {dest.resolve()}')
print('Read datacenter-construction/PORTABLE-RESTORE-NOTES.md. Hourly automation remains OFF; no jobs were started.')
