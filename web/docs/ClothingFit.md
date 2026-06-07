# Clothing: Fit

Tag-toggle node under the `utility/text` category.
Internal layer / category: `clothing` / `clothing.fit`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `preset` (combo): `custom` (use the checkboxes), `all_on`, `all_off`, `invert`.
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `prompt` (STRING): selected tags joined by `separator`.
- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `skin_tight`
- `form_fitting`
- `impossible_clothes`
- `impossible_shirt`
- `impossible_dress`
- `impossible_leotard`
- `impossible_swimsuit`
- `impossible_bodysuit`
- `tight_clothes`
- `tight_top`
- `tight_shirt`
- `tight_dress`
- `tight_pants`
- `tight_bottoms`
- `tight_jacket`
- `taut_clothes`
- `taut_shirt`
- `taut_dress`
- `taut_skirt`
- `taut_shorts`
- `taut_jacket`
- `taut_sweater`
- `taut_sweater_vest`
- `taut_vest`
- `taut_camisole`
- `taut_bandeau`
- `taut_leotard`
- `taut_bodysuit`
- `taut_bodystocking`
- `taut_swimsuit`
- `taut_bikini`
- `loose_clothes`
- `loose_shirt`
- `loose_pants`
- `baggy_clothes`
- `baggy_pants`
- `oversized_clothes`
- `oversized_shirt`
- `bursting_breasts`
- `button_gap`
- `popped_button`
- `undersized_clothes`
- `bodysuit`
- `catsuit`
- `unitard`
- `bikesuit`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
- The `prompt` output is convenient when you only need this one node and want to drop it straight into a `TextConcat`.
