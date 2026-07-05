# Meta: Subject Count (solo/duo/group)

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
**Mutex node** — only one of the toggled tags survives after `TagsBuild`.
Internal layer / category: `meta` / `meta.count.total`.

## Inputs

- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsBuild` (carries category + mutex metadata).

## Tags

- `solo`
- `solo_focus`
- `duo`
- `trio`
- `group`
- `pov`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsBuild` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
