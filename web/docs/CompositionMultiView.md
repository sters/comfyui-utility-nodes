# Composition: Multi-View

Tag-toggle node under the `utility/text` category.
Internal layer / category: `composition` / `composition.multi_view`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `preset` (combo): `custom` (use the checkboxes), `all_on`, `all_off`, `invert`.
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `prompt` (STRING): selected tags joined by `separator`.
- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `multiple_views`
- `reference_sheet`
- `character_chart`
- `turnaround`
- `sprite_sheet`
- `multiple_expressions`
- `variations`
- `projected_inset`
- `zoom_layer`
- `age_comparison`
- `clothes_on_and_off`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
- The `prompt` output is convenient when you only need this one node and want to drop it straight into a `TextConcat`.
