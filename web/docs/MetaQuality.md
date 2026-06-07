# Meta: Quality (defaults all-on)

Tag-toggle node under the `utility/text` category.
All tags default to **ON** (use the `preset` selector or individual toggles to turn things off).
Internal layer / category: `meta` / `meta.quality`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `preset` (combo): `custom` (use the checkboxes), `all_on`, `all_off`, `invert`.
- One BOOLEAN toggle per tag below (default: `True`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `prompt` (STRING): selected tags joined by `separator`.
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
- The `prompt` output is convenient when you only need this one node and want to drop it straight into a `TextConcat`.
