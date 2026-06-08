# Bad: Quality

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
All tags default to **ON** (use `invert` or the individual toggles to turn things off).
Internal layer / category: `bad` / `bad.quality`.

The negative-prompt counterpart to **Meta: Quality** — the `worst quality, low
quality, lowres, ...` fidelity/artifact/overlay staples you put on the negative
side. Distinct from **Bad: General** and friends, which cover `bad_anatomy`-style
*structural* errors rather than overall image quality.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `True`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `worst_quality`
- `low_quality`
- `normal_quality`
- `bad_quality`
- `lowres`
- `jpeg_artifacts`
- `compression_artifacts`
- `blurry`
- `watermark`
- `signature`
- `username`
- `artist_name`
- `text`
- `logo`
- `error`
- `chromatic_aberration`

## Notes

- Wire `bundle` into the **negative** `TagsMerge` (alongside `Bad: General` etc.), then that `TagsMerge`'s `prompt` into your negative `CLIPTextEncode`.
- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
