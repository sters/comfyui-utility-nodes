# Body: Moles & Freckles

Tag-toggle node under the `utility/text` category.
Internal layer / category: `anatomy` / `body.marks.moles`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `preset` (combo): `custom` (use the checkboxes), `all_on`, `all_off`, `invert`.
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `prompt` (STRING): selected tags joined by `separator`.
- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

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

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
- The `prompt` output is convenient when you only need this one node and want to drop it straight into a `TextConcat`.
