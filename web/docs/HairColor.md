# Hair: Color

Tag-toggle node under the `utility/text` category.
Internal layer / category: `anatomy` / `body.hair.color`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `preset` (combo): `custom` (use the checkboxes), `all_on`, `all_off`, `invert`.
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `prompt` (STRING): selected tags joined by `separator`.
- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `blonde_hair`
- `black_hair`
- `brown_hair`
- `blue_hair`
- `light_blue_hair`
- `pink_hair`
- `white_hair`
- `grey_hair`
- `silver_hair`
- `purple_hair`
- `red_hair`
- `green_hair`
- `orange_hair`
- `aqua_hair`
- `multicolored_hair`
- `two-tone_hair`
- `streaked_hair`
- `gradient_hair`
- `colored_inner_hair`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
- The `prompt` output is convenient when you only need this one node and want to drop it straight into a `TextConcat`.
