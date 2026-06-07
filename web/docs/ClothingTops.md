# Clothing: Tops

Tag-toggle node under the `utility/text` category.
Internal layer / category: `clothing` / `clothing.tops`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `preset` (combo): `custom` (use the checkboxes), `all_on`, `all_off`, `invert`.
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `prompt` (STRING): selected tags joined by `separator`.
- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `shirt`
- `t-shirt`
- `dress_shirt`
- `blouse`
- `collared_shirt`
- `polo_shirt`
- `tank_top`
- `camisole`
- `crop_top`
- `tube_top`
- `off-shoulder_shirt`
- `sleeveless_shirt`
- `frilled_shirt`
- `sweater`
- `turtleneck`
- `ribbed_sweater`
- `sweater_vest`
- `hoodie`
- `cardigan`
- `vest`
- `waistcoat`
- `jacket`
- `blazer`
- `coat`
- `trench_coat`
- `long_coat`
- `winter_coat`
- `raincoat`
- `windbreaker`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
- The `prompt` output is convenient when you only need this one node and want to drop it straight into a `TextConcat`.
