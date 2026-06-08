# Clothing: Pattern

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
Internal layer / category: `clothing` / `clothing.pattern`.

## Inputs

- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `striped`
- `vertical_stripes`
- `horizontal_stripes`
- `diagonal_stripes`
- `striped_clothes`
- `polka_dot`
- `plaid`
- `checkered`
- `checkered_clothes`
- `argyle`
- `houndstooth`
- `floral_print`
- `leaf_print`
- `star_print`
- `heart_print`
- `animal_print`
- `leopard_print`
- `zebra_print`
- `camouflage`
- `tie-dye`
- `gradient_clothes`
- `two-tone_clothes`
- `multicolored_clothes`
- `print_shirt`
- `print_dress`
- `print_skirt`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
