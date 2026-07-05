# Face / Eyes: Color

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
Internal layer / category: `anatomy` / `body.face.eyes.color`.

## Inputs

- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsBuild` (carries category + mutex metadata).

## Tags

- `blue_eyes`
- `red_eyes`
- `brown_eyes`
- `green_eyes`
- `purple_eyes`
- `violet_eyes`
- `yellow_eyes`
- `gold_eyes`
- `orange_eyes`
- `pink_eyes`
- `black_eyes`
- `grey_eyes`
- `aqua_eyes`
- `white_eyes`
- `multicolored_eyes`
- `heterochromia`
- `gradient_eyes`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsBuild` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
