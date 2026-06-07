# Clothing: State

Tag-toggle node under the `utility/text` category.
Internal layer / category: `clothing` / `clothing.state`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `preset` (combo): `custom` (use the checkboxes), `all_on`, `all_off`, `invert`.
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `prompt` (STRING): selected tags joined by `separator`.
- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `topless`
- `bottomless`
- `no_panties`
- `undressing`
- `dressing`
- `half-undressed`
- `open_clothes`
- `open_shirt`
- `open_jacket`
- `open_coat`
- `open_robe`
- `open_kimono`
- `open_dress`
- `open_vest`
- `open_cardigan`
- `partially_unbuttoned`
- `unbuttoned`
- `untied`
- `loose_necktie`
- `wardrobe_malfunction`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
- The `prompt` output is convenient when you only need this one node and want to drop it straight into a `TextConcat`.
