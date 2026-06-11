# Body: Animal Wings

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
**Mutex node** — only one of the toggled tags survives after `TagsMerge`.
Internal layer / category: `anatomy` / `body.animal.wings`.

## Inputs

- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `wings`
- `angel_wings`
- `demon_wings`
- `fairy_wings`
- `bat_wings`
- `butterfly_wings`
- `dragon_wings`
- `feathered_wings`
- `insect_wings`
- `mechanical_wings`
- `small_wings`
- `large_wings`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
