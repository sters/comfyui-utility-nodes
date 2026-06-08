# Clothing: Bottoms

Tag-toggle node under the `utility/text` category.
Internal layer / category: `clothing` / `clothing.bottoms`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `skirt`
- `miniskirt`
- `long_skirt`
- `pleated_skirt`
- `high-waist_skirt`
- `frilled_skirt`
- `pencil_skirt`
- `tutu`
- `hakama_skirt`
- `pants`
- `jeans`
- `denim_pants`
- `leggings`
- `harem_pants`
- `wide-leg_pants`
- `cargo_pants`
- `track_pants`
- `shorts`
- `short_shorts`
- `hot_pants`
- `denim_shorts`
- `bike_shorts`
- `bloomers`
- `overalls`
- `suspenders`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
