# Scene: Lighting

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
Internal layer / category: `scene` / `scene.lighting`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `backlighting`
- `rim_lighting`
- `soft_lighting`
- `hard_lighting`
- `dramatic_lighting`
- `cinematic_lighting`
- `volumetric_lighting`
- `ambient_lighting`
- `studio_lighting`
- `natural_lighting`
- `harsh_lighting`
- `dappled_sunlight`
- `sunlight`
- `moonlight`
- `candlelight`
- `lamp_light`
- `neon_lights`
- `neon_trim`
- `lens_flare`
- `god_rays`
- `light_rays`
- `sun_dappling`
- `silhouette`
- `chiaroscuro`
- `low_key`
- `high_key`
- `spotlight`
- `rim_light`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
