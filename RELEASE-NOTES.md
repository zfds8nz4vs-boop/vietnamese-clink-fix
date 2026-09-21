# Vietnamese Clink Fix — v1.0.0

First release of the Vietnamese community pack.

Included:
- `vi.clex`: CLEX v1 Vietnamese dictionary built with the upstream-compatible builder.
- `vi.cngm`: CNGM v1 next-word model from Vietnamese Tatoeba sentences.
- `vi.cime`: Vietnamese Telex reading-to-candidate table.
- `vi.emoji.json`: Vietnamese emoji aliases and stopwords.
- `manifest.json`: release manifest with SHA-256 and byte counts.

Telex coverage explicitly tests tone placement, old/new spelling aliases,
đ/Đ, ươ/ưo handling, repeated letters, repeated w, and repeated tone keys.

This release is generated in GitHub Actions from pinned public source URLs.
