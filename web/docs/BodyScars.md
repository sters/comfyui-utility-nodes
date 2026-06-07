# Body: Scars

Tag-toggle node under the `utility/text` category.
Internal layer / category: `anatomy` / `body.marks.scars`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `preset` (combo): `custom` (use the checkboxes), `all_on`, `all_off`, `invert`.
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `prompt` (STRING): selected tags joined by `separator`.
- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `scar`
- `scar_on_face`
- `scar_on_cheek`
- `scar_across_eye`
- `scar_on_nose`
- `scar_on_forehead`
- `scar_on_arm`
- `scar_on_chest`
- `scar_on_stomach`
- `scar_on_back`
- `scar_on_neck`
- `scar_on_leg`
- `bandages`
- `bandaged_arm`
- `bandaged_leg`
- `bandage_over_one_eye`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
- The `prompt` output is convenient when you only need this one node and want to drop it straight into a `TextConcat`.
