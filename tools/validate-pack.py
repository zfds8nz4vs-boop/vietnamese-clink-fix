#!/usr/bin/env python3
import json,pathlib,struct,sys
if len(sys.argv)!=2: raise SystemExit("Usage: python3 tools/validate-pack.py <code>")
code=sys.argv[1]; root=pathlib.Path("Lexicons"); errors=[]
clex=root/f"{code}.clex"; cngm=root/f"{code}.cngm"
if not clex.exists(): errors.append(f"Missing {clex}")
else:
    d=clex.read_bytes()
    if len(d)<16 or d[:4]!=b"CLEX" or struct.unpack_from("<I",d,4)[0]!=1: errors.append("Invalid CLEX v1")
if cngm.exists():
    d=cngm.read_bytes()
    if len(d)<12 or d[:4]!=b"CNGM" or struct.unpack_from("<I",d,4)[0]!=1: errors.append("Invalid CNGM v1")
cime=root/f"{code}.cime"
if cime.exists() and not cime.read_text(encoding="utf-8").strip(): errors.append("Empty CIME")
emoji=root/f"{code}.emoji.json"
if emoji.exists():
    try:
        m=json.loads(emoji.read_text(encoding="utf-8"))
        if m.get("version")!=1: errors.append("Emoji metadata version must be 1")
        if not isinstance(m.get("aliases"),dict): errors.append("Emoji aliases must be an object")
        if not isinstance(m.get("stopwords"),list): errors.append("Emoji stopwords must be an array")
    except Exception as e: errors.append(f"Invalid emoji JSON: {e}")
if errors: raise SystemExit("\n".join("ERROR: "+e for e in errors))
print(f"{code}: looks ready for release.")
