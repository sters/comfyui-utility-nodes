# Composition: Crop

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
Internal layer / category: `composition` / `composition.crop`.

## Inputs

- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `cropped_legs`
- `cropped_torso`
- `cropped_arms`
- `cropped_shoulders`
- `cropped_head`
- `head_out_of_frame`
- `feet_out_of_frame`
- `eyes_out_of_frame`
- `foot_out_of_frame`
- `knees_out_of_frame`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
