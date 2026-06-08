# Clothing: Material

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
Internal layer / category: `clothing` / `clothing.material`.

## Inputs

- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

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
