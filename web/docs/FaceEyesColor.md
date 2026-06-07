# Face / Eyes: Color

Tag-toggle node under the `utility/text` category.
Internal layer / category: `anatomy` / `body.face.eyes.color`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `preset` (combo): `custom` (use the checkboxes), `all_on`, `all_off`, `invert`.
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `prompt` (STRING): selected tags joined by `separator`.
- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

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

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
- The `prompt` output is convenient when you only need this one node and want to drop it straight into a `TextConcat`.
