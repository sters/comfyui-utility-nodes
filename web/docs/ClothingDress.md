# Clothing: Dress & One-piece

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
**Mutex node** — only one of the toggled tags survives after `TagsMerge`.
Internal layer / category: `clothing` / `clothing.dress`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `dress`
- `sundress`
- `long_dress`
- `short_dress`
- `evening_gown`
- `ball_gown`
- `wedding_dress`
- `off-shoulder_dress`
- `halter_dress`
- `pinafore_dress`
- `frilled_dress`
- `kimono`
- `yukata`
- `furisode`
- `hakama`
- `qipao`
- `china_dress`
- `hanfu`
- `ao_dai`
- `sari`
- `robe`
- `jumpsuit`
- `romper`
- `leotard`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
