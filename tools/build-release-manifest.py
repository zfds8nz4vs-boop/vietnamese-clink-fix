#!/usr/bin/env python3
import hashlib,json,pathlib,shutil,sys
def ok(p): return p.is_file() and not p.name.startswith("._") and p.name!=".DS_Store"
if len(sys.argv)!=4: raise SystemExit("usage: build-release-manifest.py VERSION OWNER/REPO OUT")
version,repo,out=sys.argv[1:]; root=pathlib.Path(__file__).resolve().parents[1]; lex=root/"Lexicons"; dest=pathlib.Path(out); assets=dest/"assets"; packs=[]
for clex in sorted(lex.glob("*.clex")):
    code=clex.stem; entries=[]
    for p in sorted(lex.glob(code+".*")):
        for f in (p.rglob("*") if p.is_dir() else [p]):
            if not ok(f): continue
            rel=f.relative_to(lex).as_posix(); name=code+"--"+rel.replace("/","--"); target=assets/name; target.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(f,target)
            d=target.read_bytes(); entries.append({"path":rel,"url":f"https://github.com/{repo}/releases/download/{version}/{name}","sha256":hashlib.sha256(d).hexdigest(),"byteCount":len(d)})
    packs.append({"code":code,"version":version,"assets":entries})
dest.mkdir(parents=True,exist_ok=True); (dest/"manifest.json").write_text(json.dumps({"version":version,"packs":packs},separators=(",",":")),encoding="utf-8")
