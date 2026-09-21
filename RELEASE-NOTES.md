# Vietnamese Clink Fix — v1.0.1

Corrected first public release, superseding v1.0.0.

Included:
- `vi.clex`: 47,410-word Vietnamese CLEX v1 dictionary.
- `vi.cngm`: 67,778 next-word pairs from Vietnamese Tatoeba sentences.
- `vi.cime`: 53,230 Telex readings/candidate rows.
- `vi.emoji.json`: Vietnamese emoji aliases and stopwords.
- `manifest.json`: release manifest with SHA-256 and byte counts.

Telex regression coverage includes tone placement, modern/traditional aliases,
đ/Đ, ươ/ưo handling, repeated letters, repeated w, repeated tone keys, and
nonstandard decomposed Unicode input tolerance.

The v1.0.0 build was generated successfully but omitted the checked-in emoji
metadata because its CI cleanup removed the metadata before packaging. v1.0.1
fixes that packaging defect and is the release to use.
