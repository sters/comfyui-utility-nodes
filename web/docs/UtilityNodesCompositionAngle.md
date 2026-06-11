# Composition: Angle

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
**Mutex node** — only one of the toggled tags survives after `TagsMerge`.
Internal layer / category: `composition` / `composition.angle`.

## Inputs

- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `dutch_angle`
- `from_above`
- `from_behind`
- `from_below`
- `from_side`
- `sideways`
- `three-quarter_view`
- `straight-on`
- `upside-down`
- `pov`
- `from_outside`
- `from_inside`
- `partially_underwater_shot`
- `atmospheric_perspective`
- `fisheye`
- `perspective`
- `vanishing_point`
- `foreshortening`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
