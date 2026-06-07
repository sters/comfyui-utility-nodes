# Clothing: Position (displacement)

Tag-toggle node under the `utility/text` category.
Internal layer / category: `clothing` / `clothing.position`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `preset` (combo): `custom` (use the checkboxes), `all_on`, `all_off`, `invert`.
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `prompt` (STRING): selected tags joined by `separator`.
- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `goggles_on_head`
- `glasses_on_head`
- `sunglasses_on_head`
- `hood_up`
- `hood_down`
- `headphones_around_neck`
- `mask_pull`
- `mask_down`
- `mask_up`
- `hat_over_eyes`
- `hat_tip`
- `jacket_on_shoulders`
- `coat_on_shoulders`
- `jacket_partially_removed`
- `off_shoulder`
- `single_off_shoulder`
- `clothes_around_waist`
- `shirt_around_waist`
- `scarf_over_mouth`
- `necktie_over_shoulder`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
- The `prompt` output is convenient when you only need this one node and want to drop it straight into a `TextConcat`.
