# Clothing: Accessory (other)

Tag-toggle node under the `utility/text` category.
Internal layer / category: `clothing` / `clothing.accessory.other`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `preset` (combo): `custom` (use the checkboxes), `all_on`, `all_off`, `invert`.
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `prompt` (STRING): selected tags joined by `separator`.
- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `earrings`
- `single_earring`
- `ear_piercing`
- `stud_earrings`
- `hoop_earrings`
- `drop_earrings`
- `belt`
- `waist_cape`
- `obi`
- `sash`
- `belt_pouch`
- `apron`
- `frilled_apron`
- `waist_apron`
- `bag`
- `handbag`
- `shoulder_bag`
- `backpack`
- `satchel`
- `school_bag`
- `umbrella`
- `parasol`
- `fan`
- `folding_fan`
- `lip_piercing`
- `nose_piercing`
- `navel_piercing`
- `tongue_piercing`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
- The `prompt` output is convenient when you only need this one node and want to drop it straight into a `TextConcat`.
