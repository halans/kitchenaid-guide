#!/usr/bin/env python3
"""Verify bundled bytes, freshness and tests entirely offline."""
import hashlib,pathlib,json,subprocess,sys
root=pathlib.Path(__file__).resolve().parent
expected=json.loads((root/'checksums.json').read_text());bad=[]
for name,digest in expected.items():
 p=root/name
 if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:bad.append(name)
if bad:print('FAILED checksums: '+', '.join(bad));sys.exit(1)
print(f'Checksums OK: {len(expected)} files',flush=True)
for command in [[sys.executable,str(root/'build.py'),'--check'],[sys.executable,str(root/'test.py')]]:
 r=subprocess.run(command,cwd=root)
 if r.returncode:sys.exit(r.returncode)
print('PASS: bundle verified, both builds current, all structural/equivalence tests passed.')
