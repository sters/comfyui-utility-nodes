# Meta: Quality

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
All tags default to **OFF** — anime-style prompts don't want `realistic` / `photorealistic` baked in, so pick the quality boosters you actually want per workflow (or set `invert` to grab everything except a few).
Internal layer / category: `meta` / `meta.quality`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `masterpiece`
- `best_quality`
- `high_quality`
- `highres`
- `absurdres`
- `ultra-detailed`
- `ultra_high_res`
- `ultra_realistic`
- `intricate_details`
- `fine_details`
- `detailed_background`
- `official_art`
- `photorealistic`
- `realistic`
- `8k`
- `4k`
- `newest`
- `very_aesthetic`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
