# NSFW Act: Penetrative

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
**Mutex node** — only one of the toggled tags survives after `TagsMerge`.
Internal layer / category: `nsfw_act` / `nsfw.act.penetrative`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `sex`
- `vaginal`
- `anal`
- `double_penetration`
- `triple_penetration`
- `deepthroat`
- `vaginal_object_insertion`
- `anal_object_insertion`
- `fingering`
- `vaginal_fingering`
- `anal_fingering`
- `rough_sex`
- `sex_from_behind`
- `imminent_penetration`
- `spitroast`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
