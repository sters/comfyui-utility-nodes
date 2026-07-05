# Body: Animal Horns

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
**Mutex node** — only one of the toggled tags survives after `TagsBuild`.
Internal layer / category: `anatomy` / `body.animal.horns`.

## Inputs

- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsBuild` (carries category + mutex metadata).

## Tags

- `horns`
- `single_horn`
- `multiple_horns`
- `demon_horns`
- `devil_horns`
- `oni_horns`
- `dragon_horns`
- `deer_horns`
- `ram_horns`
- `curled_horns`
- `antlers`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsBuild` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
