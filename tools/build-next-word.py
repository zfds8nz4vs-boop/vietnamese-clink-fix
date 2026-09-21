#!/usr/bin/env python3
"""Build a Clink CNGM v1 next-word model from a sentence corpus."""
import collections,math,pathlib,re,struct,sys,unicodedata
if len(sys.argv)!=4: raise SystemExit("Usage: python3 tools/build-next-word.py <code> <word-list.txt> <sentences.txt>")
code,word_path,corpus_path=sys.argv[1],pathlib.Path(sys.argv[2]),pathlib.Path(sys.argv[3])
if not code or not code.replace("_","").replace("-","").isalnum(): raise SystemExit("Invalid language code.")
def word(v):
    v=unicodedata.normalize("NFC",v.strip().lower())
    return v if v and not any(c.isspace() for c in v) and any(c.isalpha() for c in v) else None
words=set()
for raw in word_path.read_text(encoding="utf-8").splitlines():
    if raw.strip() and not raw.lstrip().startswith("#"):
        x=word(raw.rsplit(maxsplit=1)[0])
        if x: words.add(x)
ordered=sorted(words,key=lambda x:x.encode("utf-8")); ids={w:i for i,w in enumerate(ordered)}
pairs=collections.Counter()
for raw in corpus_path.read_text(encoding="utf-8").splitlines():
    sentence=raw.rsplit("\t",1)[-1]
    toks=[word(t) for t in re.findall(r'[^\s.,!?;:"“”‘’()\[\]{}]+',sentence)]
    toks=[t for t in toks if t in ids]; pairs.update(zip(toks,toks[1:]))
if not pairs: raise SystemExit("No word pairs matched the word list.")
totals=collections.Counter()
for (a,_),c in pairs.items(): totals[a]+=c
ranked=sorted(pairs.items(),key=lambda item:(ids[item[0][0]],-item[1],ids[item[0][1]]))
blob=bytearray(b"CNGM"+struct.pack("<II",1,len(ranked)))
for (a,_),_ in ranked: blob+=struct.pack("<I",ids[a])
for (_,b),_ in ranked: blob+=struct.pack("<I",ids[b])
for (a,_),c in ranked:
    p=c/totals[a]; blob.append(max(0,min(255,round((math.log10(p)+6)*42))))
out=pathlib.Path("Lexicons")/f"{code}.cngm"; out.parent.mkdir(exist_ok=True); out.write_bytes(blob)
print(f"Built {out} with {len(ranked):,} next-word pairs.")
