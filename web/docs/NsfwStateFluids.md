# NSFW State: Fluids

Tag-toggle node under the `utility/text` category.
Internal layer / category: `nsfw_state` / `nsfw.state.fluids`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `preset` (combo): `custom` (use the checkboxes), `all_on`, `all_off`, `invert`.
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `prompt` (STRING): selected tags joined by `separator`.
- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `cum`
- `cum_in_pussy`
- `cum_in_ass`
- `cum_in_mouth`
- `cum_in_nose`
- `cum_on_body`
- `cum_on_face`
- `cum_on_breasts`
- `cum_on_stomach`
- `cum_on_hair`
- `cum_on_ass`
- `cum_on_self`
- `cum_string`
- `facial`
- `ejaculation`
- `ejaculating_while_penetrated`
- `excessive_cum`
- `overflow`
- `female_ejaculation`
- `squirting`
- `pussy_juice`
- `pussy_juice_trail`
- `saliva`
- `saliva_trail`
- `tears`
- `sweat`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
- The `prompt` output is convenient when you only need this one node and want to drop it straight into a `TextConcat`.
