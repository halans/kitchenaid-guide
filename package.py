#!/usr/bin/env python3
import pathlib,hashlib,json,zipfile,argparse
root=pathlib.Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--manifest-only',action='store_true');args=ap.parse_args()
def files():return sorted(p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and '.git' not in p.parts and p.relative_to(root).parts[:2]!=('dist','assets') and p.suffix not in ['.pyc','.zip'])
manifest={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files() if p.name!='checksums.json'}
(root/'checksums.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n');print(f'Manifest: {len(manifest)} files')
if not args.manifest_only:
 target=root.parent/'beyond-the-bowl-offline.zip'
 with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in files():
   info=zipfile.ZipInfo('kitchenaid-guide/'+str(p.relative_to(root)),date_time=(2026,10,4,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,p.read_bytes())
 print(f'Created {target.name} ({target.stat().st_size:,} bytes)')
