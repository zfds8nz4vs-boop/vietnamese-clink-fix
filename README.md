# Vietnamese Clink Fix

A Vietnamese community language pack for Clink, built to follow the resource-oriented structure of
[anti-ltd/clink-language-packs](https://github.com/anti-ltd/clink-language-packs).

## What this pack contains

| Asset | Purpose |
|---|---|
| `vi.clex` | Vietnamese dictionary/completion data |
| `vi.cngm` | next-word prediction |
| `vi.cime` | Vietnamese Telex reading → candidate conversion |
| `vi.emoji.json` | Vietnamese emoji aliases and stopwords |
| `manifest.json` | release metadata, hashes and byte counts |

The dictionary and next-word model are generated with the same CLEX1/CNGM1 layout used by the
reference language-pack project. The Telex table is generated as a CIME reading→candidate asset.

## Vietnamese Telex behavior

The pack explicitly covers the common UniKey-style Telex conventions:

- `aa → â`, `aw → ă`, `ee → ê`, `oo → ô`, `ow → ơ`, `uw → ư`, `dd → đ`
- tone keys `s f r x j`
- Vietnamese tone placement for nuclei such as `tiếng, Việt, đường, người, bài, chiều, chuối, nước, biển, quyền`
- modern/common and traditional tone-position aliases where both are encountered
- literal escape rows for repeated letters and repeated tone keys
- explicit `uww → ưw`, `oww → ơw`, `aww → ăw` preservation forms

The static CIME table cannot observe key timing, so literal escape readings are encoded explicitly rather than pretending to implement a stateful IME inside CIME.

## Reproducible build

The release workflow downloads:
- FrequencyWords Vietnamese 50k word list
- Tatoeba Vietnamese sentence export

Then it runs:

```sh
python3 build-pack.py vi source/vi_50k.txt
python3 tools/build-next-word.py vi source/vi_50k.txt source/vie_sentences.tsv
python3 tools/build-telex-cime.py vi source/vi_50k.txt
python3 tools/test_telex_rules.py
python3 tools/validate-pack.py vi
python3 tools/build-release-manifest.py v1.0.1 zfds8nz4vs-boop/vietnamese-clink-fix release
```

The raw downloaded inputs are build inputs, not release assets.

## Provenance

See `NOTICE.md`, `LICENSE.md`, and `catalog/language-wave.json`.
