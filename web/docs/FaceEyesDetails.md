# Face / Eyes: Pupils & Details

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
Internal layer / category: `anatomy` / `body.face.eyes.details`.

## Inputs

- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `heart-shaped_pupils`
- `star-shaped_pupils`
- `plus-shaped_pupils`
- `cross-shaped_pupils`
- `slit_pupils`
- `dot_pupils`
- `mismatched_pupils`
- `no_pupils`
- `white_pupils`
- `glowing_eyes`
- `shiny_eyes`
- `sparkling_eyes`
- `jeweled_eyes`
- `empty_eyes`
- `blank_eyes`
- `long_eyelashes`
- `thick_eyebrows`
- `thin_eyebrows`
- `aegyo_sal`
- `eyeshadow`
- `eyeliner`
- `tsurime`
- `tareme`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
