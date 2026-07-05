# Clothing: Tops

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
Internal layer / category: `clothing` / `clothing.tops`.

## Inputs

- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsBuild` (carries category + mutex metadata).

## Tags

- `shirt`
- `t-shirt`
- `dress_shirt`
- `blouse`
- `collared_shirt`
- `polo_shirt`
- `tank_top`
- `camisole`
- `crop_top`
- `tube_top`
- `off-shoulder_shirt`
- `sleeveless_shirt`
- `frilled_shirt`
- `sweater`
- `turtleneck`
- `ribbed_sweater`
- `sweater_vest`
- `hoodie`
- `cardigan`
- `vest`
- `waistcoat`
- `jacket`
- `blazer`
- `coat`
- `trench_coat`
- `long_coat`
- `winter_coat`
- `raincoat`
- `windbreaker`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsBuild` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
