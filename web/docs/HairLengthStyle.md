# Hair: Length & Style

Tag-toggle node under the `utility/text` category.
Internal layer / category: `anatomy` / `body.hair.length_style`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `preset` (combo): `custom` (use the checkboxes), `all_on`, `all_off`, `invert`.
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `prompt` (STRING): selected tags joined by `separator`.
- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `very_long_hair`
- `long_hair`
- `medium_hair`
- `short_hair`
- `short_hair_with_long_locks`
- `low-tied_long_hair`
- `ponytail`
- `high_ponytail`
- `low_ponytail`
- `side_ponytail`
- `twintails`
- `low_twintails`
- `short_twintails`
- `twin_braids`
- `side_braid`
- `single_braid`
- `braid`
- `bob_cut`
- `hair_bun`
- `double_bun`
- `single_hair_bun`
- `drill_hair`
- `twin_drills`
- `one_side_up`
- `two_side_up`
- `half_updo`
- `wavy_hair`
- `straight_hair`
- `curly_hair`
- `messy_hair`
- `spiked_hair`
- `floating_hair`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
- The `prompt` output is convenient when you only need this one node and want to drop it straight into a `TextConcat`.
