# Scene: Indoor Location

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
Internal layer / category: `scene` / `scene.indoor`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `indoors`
- `classroom`
- `school`
- `kitchen`
- `bedroom`
- `bathroom`
- `shower`
- `bathtub`
- `library`
- `hospital`
- `office`
- `gym`
- `cafe`
- `restaurant`
- `bar`
- `train_interior`
- `car_interior`
- `dressing_room`
- `locker_room`
- `shrine`
- `church`
- `club`
- `casino`
- `stage`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
