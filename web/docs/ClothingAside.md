# Clothing: Aside & Partial Expose

Tag-toggle node under the `utility/text` category.
Internal layer / category: `clothing` / `clothing.aside`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `preset` (combo): `custom` (use the checkboxes), `all_on`, `all_off`, `invert`.
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `prompt` (STRING): selected tags joined by `separator`.
- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `clothing_aside`
- `panties_aside`
- `thong_aside`
- `panties_under_pantyhose_aside`
- `male_underwear_aside`
- `fundoshi_aside`
- `loincloth_aside`
- `pelvic_curtain_aside`
- `bra_aside`
- `bikini_aside`
- `bikini_top_aside`
- `bikini_bottom_aside`
- `swimsuit_aside`
- `leotard_aside`
- `dress_aside`
- `shirt_aside`
- `skirt_aside`
- `shorts_aside`
- `buruma_aside`
- `apron_aside`
- `necktie_aside`
- `strap_slip`
- `double_strap_slip`
- `suspenders_slip`
- `shoulder_strap_slip`
- `shirt_slip`
- `breast_slip`
- `one_breast_out`
- `one_side_pulled_down`
- `exposed_gusset`
- `pulled_by_self`
- `pulled_by_another`
- `accidental_exposure`
- `assisted_exposure`
- `wind_lift`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
- The `prompt` output is convenient when you only need this one node and want to drop it straight into a `TextConcat`.
