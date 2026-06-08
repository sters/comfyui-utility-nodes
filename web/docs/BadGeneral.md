# Bad: General

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
All tags default to **ON** (use `invert` or the individual toggles to turn things off).
Internal layer / category: `bad` / `bad.general`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `True`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `artistic_error`
- `bad_anatomy`
- `anatomical_nonsense`
- `bad_proportions`
- `bad_perspective`
- `bad_reflection`
- `bad_multiple_views`
- `bad_shadow`
- `bad_gun_anatomy`
- `bad_vehicle_anatomy`
- `bad_internal_anatomy`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
