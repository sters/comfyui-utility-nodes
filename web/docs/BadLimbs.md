# Bad: Limbs

Tag-toggle node under the `utility/text` category.
All tags default to **ON** (use the `preset` selector or individual toggles to turn things off).
Internal layer / category: `bad` / `bad.limbs`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `preset` (combo): `custom` (use the checkboxes), `all_on`, `all_off`, `invert`.
- One BOOLEAN toggle per tag below (default: `True`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `prompt` (STRING): selected tags joined by `separator`.
- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `bad_arm`
- `bad_hands`
- `bad_leg`
- `bad_knees`
- `bad_feet`
- `wrong_hand`
- `wrong_foot`
- `extra_digits`
- `extra_arms`
- `extra_hands`
- `extra_legs`
- `extra_toes`
- `fewer_digits`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
- The `prompt` output is convenient when you only need this one node and want to drop it straight into a `TextConcat`.
