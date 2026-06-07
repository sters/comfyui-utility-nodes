# Clothing: Material

Tag-toggle node under the `utility/text` category.
Internal layer / category: `clothing` / `clothing.material`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `preset` (combo): `custom` (use the checkboxes), `all_on`, `all_off`, `invert`.
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `prompt` (STRING): selected tags joined by `separator`.
- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `see-through`
- `see-through_silhouette`
- `transparent`
- `wet_clothes`
- `torn_clothes`
- `lace`
- `lace_trim`
- `frilled`
- `frills`
- `ribbed`
- `knit`
- `mesh`
- `fishnets`
- `denim`
- `leather`
- `latex`
- `rubber`
- `vinyl`
- `silk`
- `satin`
- `velvet`
- `fur`
- `fur_trim`
- `wool`
- `metallic`
- `shiny_clothes`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
- The `prompt` output is convenient when you only need this one node and want to drop it straight into a `TextConcat`.
