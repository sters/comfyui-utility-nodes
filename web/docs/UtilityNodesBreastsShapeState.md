# Breasts: Shape & State

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
Internal layer / category: `anatomy` / `body.breasts.shape_state`.

## Inputs

- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsBuild` (carries category + mutex metadata).

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

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsBuild` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
