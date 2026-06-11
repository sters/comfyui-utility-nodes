# Body: Figure

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
Internal layer / category: `anatomy` / `body.figure`.

## Inputs

- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `petite`
- `slim`
- `curvy`
- `toned`
- `muscular`
- `muscular_female`
- `muscular_male`
- `abs`
- `toned_female`
- `toned_male`
- `thick_thighs`
- `wide_hips`
- `thigh_gap`
- `skindentation`
- `pectorals`
- `large_pectorals`
- `narrow_waist`
- `plump`
- `chubby`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
