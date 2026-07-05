# Clothing: State

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
Internal layer / category: `clothing` / `clothing.state`.

## Inputs

- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsBuild` (carries category + mutex metadata).

## Tags

- `topless`
- `bottomless`
- `no_panties`
- `undressing`
- `dressing`
- `half-undressed`
- `open_clothes`
- `open_shirt`
- `open_jacket`
- `open_coat`
- `open_robe`
- `open_kimono`
- `open_dress`
- `open_vest`
- `open_cardigan`
- `partially_unbuttoned`
- `unbuttoned`
- `untied`
- `loose_necktie`
- `wardrobe_malfunction`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsBuild` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
