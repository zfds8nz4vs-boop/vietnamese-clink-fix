#!/usr/bin/env python3
"""Generate Vietnamese Telex reading -> candidate data for Clink CIME."""
import pathlib,sys,unicodedata
if len(sys.argv)!=3: raise SystemExit("Usage: build-telex-cime.py vi <word-list.txt>")
code,source=sys.argv[1],pathlib.Path(sys.argv[2])
if code!="vi": raise SystemExit("This builder targets vi.")
TONE={"\u0301":"s","\u0300":"f","\u0309":"r","\u0303":"x","\u0323":"j"}
VOWELS=set("aăâeêioôơuưy")
SHAPE={"a":"aa","e":"ee","o":"oo","ă":"aw","ơ":"ow","ư":"uw","A":"AA","E":"EE","O":"OO","Ă":"AW","Ơ":"OW","Ư":"UW"}
def vowel_label(ch):
    d=unicodedata.normalize("NFD",ch); base=d[0].lower(); marks=set(d[1:])
    if "\u0302" in marks: return {"a":"â","e":"ê","o":"ô"}.get(base,base)
    if "\u0306" in marks and base=="a": return "ă"
    if "\u031b" in marks: return "ơ" if base=="o" else "ư"
    return base
def telex_char(ch):
    if ch=="đ": return "dd",None
    if ch=="Đ": return "DD",None
    d=unicodedata.normalize("NFD",ch); base=d[0]; marks=set(d[1:]); lower=base.lower()
    if "\u0302" in marks: shape=SHAPE.get(lower, base)
    elif "\u0306" in marks: shape="aw"
    elif "\u031b" in marks: shape="ow" if lower=="o" else "uw"
    else: shape=base
    if base.isupper(): shape=shape.upper()
    tone=next((TONE[m] for m in ("\u0301","\u0300","\u0309","\u0303","\u0323") if m in marks),None)
    return shape,tone
def syllable(word):
    parts=[]; tone=None
    for ch in word:
        s,t=telex_char(ch); parts.append(s)
        if t: tone=t
    raw="".join(parts)
    # UniKey/Telex commonly contracts ưo in final-consonant syllables: đường.
    if raw.lower().find("uwow")>=0 and vowel_label(word[-1]) not in VOWELS: raw=raw.replace("uwow","uow")
    return raw+(tone or "")
def tone_pos(chars,old=False):
    vs=[i for i,c in enumerate(chars) if vowel_label(c) in VOWELS]
    if not vs:return None
    if "".join(chars[:2]).lower() in ("gi","qu") and len(vs)>1: vs=vs[1:]
    marked=[i for i in vs if vowel_label(chars[i]) in "ăâêôơư"]
    if marked:return marked[-1] if len(marked)>1 else marked[0]
    labels=[vowel_label(chars[i]) for i in vs]
    if old:
        if vs[-1] < len(chars)-1: return vs[-1]
        return vs[-2] if len(vs)>1 else vs[0]
    if len(labels)>=2 and "".join(labels[-2:]) in ("oa","oe","uy"): return vs[-1]
    return vs[-2] if len(vs)>1 else vs[0]
def reading(word,old=False):
    out=[]; buf=[]
    for ch in unicodedata.normalize("NFC",word):
        if ch.isalpha(): buf.append(ch)
        else:
            if buf: out.append(read_syllable("".join(buf),old)); buf=[]
            out.append(ch)
    if buf: out.append(read_syllable("".join(buf),old))
    return "".join(out)
def read_syllable(s,old=False):
    chars=list(s); tone=None
    for ch in chars:
        _,t=telex_char(ch)
        if t:tone=t
    if not tone:return syllable(s)
    pos=tone_pos(chars,old); out=[]
    for i,ch in enumerate(chars):
        sh,_=telex_char(ch); out.append(sh)
        if i==pos:out.append(tone)
    return "".join(out)
def aliases(word): return list(dict.fromkeys((syllable(word),reading(word),reading(word,True))))
def add(rows,r,c):
    if not r:return
    rows.setdefault(r,[])
    if c not in rows[r]:rows[r].append(c)
    rows[r]=rows[r][:16]
def literal(rows,r):
    add(rows,r,r)
rows={}
for raw in source.read_text(encoding="utf-8").splitlines():
    raw=raw.strip()
    if not raw or raw.startswith("#"):continue
    fields=raw.rsplit(maxsplit=1); w=unicodedata.normalize("NFC",fields[0] if len(fields)==2 else raw)
    if not w or any(c.isspace() for c in w) or not any(c.isalpha() for c in w):continue
    for r in aliases(w):add(rows,r,w)
for v in "aeo":
    for n in range(3,33):literal(rows,v*n)
for base,special in (("u","ư"),("o","ơ"),("a","ă")):
    for extra in range(1,17):add(rows,base+"w"*(extra+1),special+"w"*extra)
for key in "sfrxjz":
    for n in range(2,17):literal(rows,key*n)
out=pathlib.Path("Lexicons")/f"{code}.cime"; out.parent.mkdir(exist_ok=True)
with out.open("w",encoding="utf-8",newline="\n") as f:
    for r in sorted(rows,key=str.casefold):f.write("\t".join([r,*rows[r]])+"\n")
print(f"Built {out} with {len(rows):,} readings.")
