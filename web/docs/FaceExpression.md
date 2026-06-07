# Face: Expression

Tag-toggle node under the `utility/text` category.
Internal layer / category: `anatomy` / `body.face.expression`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `preset` (combo): `custom` (use the checkboxes), `all_on`, `all_off`, `invert`.
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `prompt` (STRING): selected tags joined by `separator`.
- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `smile`
- `grin`
- `smirk`
- `smug`
- `happy`
- `laughing`
- `wry_smile`
- `embarrassed`
- `nervous`
- `shy`
- `worried`
- `confused`
- `frown`
- `scowl`
- `angry`
- `annoyed`
- `pouting`
- `sad`
- `depressed`
- `tearful`
- `surprised`
- `shocked`
- `scared`
- `frightened`
- `yandere`
- `ahegao`
- `fucked_silly`
- `serious`
- `expressionless`
- `blank_expression`
- `bored`
- `sleepy`
- `drowsy`
- `tired`
- `determined`
- `smug_grin`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
- The `prompt` output is convenient when you only need this one node and want to drop it straight into a `TextConcat`.
