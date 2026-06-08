# Scene: Particles & Atmosphere

Tag-toggle node under the `utility/text` category.
Internal layer / category: `scene` / `scene.particles`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `petals`
- `falling_petals`
- `cherry_blossoms`
- `falling_leaves`
- `autumn_leaves`
- `snowflakes`
- `fireflies`
- `sparkles`
- `glitter`
- `light_particles`
- `dust`
- `embers`
- `bubbles`
- `feathers`
- `confetti`
- `smoke`
- `steam`
- `mist`
- `fog`
- `water_drops`
- `splashing`
- `splashing_water`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
