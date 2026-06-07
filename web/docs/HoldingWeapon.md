# Body: Holding (weapon)

Tag-toggle node under the `utility/text` category.
Internal layer / category: `anatomy` / `body.holding.weapon`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `preset` (combo): `custom` (use the checkboxes), `all_on`, `all_off`, `invert`.
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `prompt` (STRING): selected tags joined by `separator`.
- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `holding_weapon`
- `holding_sword`
- `holding_katana`
- `holding_knife`
- `holding_dagger`
- `holding_gun`
- `holding_handgun`
- `holding_rifle`
- `holding_bow_(weapon)`
- `holding_arrow`
- `holding_staff`
- `holding_wand`
- `holding_polearm`
- `holding_spear`
- `holding_lance`
- `holding_scythe`
- `holding_axe`
- `holding_hammer`
- `holding_shield`
- `holding_whip`
- `holding_chain`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
- The `prompt` output is convenient when you only need this one node and want to drop it straight into a `TextConcat`.
