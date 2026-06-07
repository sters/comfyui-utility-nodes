# Breasts: Shape & State

Tag-toggle node under the `utility/text` category.
Internal layer / category: `anatomy` / `body.breasts.shape_state`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `preset` (combo): `custom` (use the checkboxes), `all_on`, `all_off`, `invert`.
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `prompt` (STRING): selected tags joined by `separator`.
- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `cleavage`
- `sideboob`
- `underboob`
- `backboob`
- `breasts_apart`
- `breast_press`
- `between_breasts`
- `covered_nipples`
- `cleavage_cutout`
- `asymmetrical_docking`
- `sagging_breasts`
- `downblouse`
- `nipples`
- `puffy_nipples`
- `inverted_nipples`
- `pointy_breasts`
- `areolae`
- `areola_slip`
- `nipple_slip`
- `breasts_out`
- `no_bra`
- `pasties`
- `nipple_piercing`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
- The `prompt` output is convenient when you only need this one node and want to drop it straight into a `TextConcat`.
