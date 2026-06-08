# Scene: Outdoor Location

Tag-toggle node under the `utility/text` category.
Internal layer / category: `scene` / `scene.outdoor`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `outdoors`
- `beach`
- `ocean`
- `lake`
- `river`
- `pool`
- `forest`
- `jungle`
- `mountain`
- `field`
- `meadow`
- `garden`
- `park`
- `street`
- `alley`
- `city`
- `skyline`
- `rooftop`
- `schoolyard`
- `playground`
- `festival`
- `snowfield`
- `desert`
- `ruins`
- `shrine_outdoors`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
