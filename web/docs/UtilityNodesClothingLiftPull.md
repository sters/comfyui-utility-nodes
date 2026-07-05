# Clothing: Lift & Pull

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
Internal layer / category: `clothing` / `clothing.lift_pull`.

## Inputs

- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsBuild` (carries category + mutex metadata).

## Tags

- `clothes_lift`
- `shirt_lift`
- `skirt_lift`
- `dress_lift`
- `kimono_lift`
- `sweater_lift`
- `hoodie_lift`
- `camisole_lift`
- `bikini_top_lift`
- `bra_lift`
- `breast_lift`
- `lifting_own_clothes`
- `lifting_another's_clothes`
- `clothes_pull`
- `panty_pull`
- `bra_pull`
- `shirt_pull`
- `skirt_pull`
- `clothes_down`
- `panties_down`
- `shirt_tug`
- `clothes_tug`
- `holding_skirt`
- `bunching_skirt`
- `clothes_held_up`
- `skirt_hold`
- `lifted_by_self`
- `lifted_by_another`
- `clothes_removed`
- `shirt_removed`
- `panties_removed`
- `bra_removed`
- `clothes_in_mouth`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsBuild` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
