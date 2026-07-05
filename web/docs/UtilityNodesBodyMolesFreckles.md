# Body: Moles & Freckles

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
Internal layer / category: `anatomy` / `body.marks.moles`.

## Inputs

- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsBuild` (carries category + mutex metadata).

## Tags

- `mole`
- `mole_under_eye`
- `mole_under_mouth`
- `mole_on_cheek`
- `mole_on_neck`
- `mole_on_breast`
- `mole_on_stomach`
- `mole_on_thigh`
- `mole_on_ass`
- `mole_on_armpit`
- `freckles`
- `beauty_mark`
- `birthmark`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsBuild` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
