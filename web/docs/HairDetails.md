# Hair: Details

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
Internal layer / category: `anatomy` / `body.hair.details`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `bangs`
- `blunt_bangs`
- `parted_bangs`
- `swept_bangs`
- `crossed_bangs`
- `double-parted_bangs`
- `hair_between_eyes`
- `hair_over_one_eye`
- `hair_over_eyes`
- `hair_over_shoulder`
- `hair_behind_ear`
- `hair_flaps`
- `sidelocks`
- `ahoge`
- `antenna_hair`
- `hair_intakes`
- `hair_tubes`
- `blunt_ends`
- `hair_ornament`
- `x_hair_ornament`
- `star_hair_ornament`
- `hair_bow`
- `hair_ribbon`
- `hair_flower`
- `hairband`
- `hairclip`
- `hair_bobbles`
- `hair_rings`
- `hair_scrunchie`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
