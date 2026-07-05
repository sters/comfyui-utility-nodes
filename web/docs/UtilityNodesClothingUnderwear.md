# Clothing: Underwear

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
Internal layer / category: `clothing` / `clothing.underwear`.

## Inputs

- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsBuild` (carries category + mutex metadata).

## Tags

- `underwear`
- `underwear_only`
- `bra`
- `sports_bra`
- `strapless_bra`
- `frilled_bra`
- `lace_bra`
- `panties`
- `thong`
- `side-tie_panties`
- `string_panties`
- `frilled_panties`
- `lace_panties`
- `boyshorts`
- `boxers`
- `briefs`
- `boxer_briefs`
- `lingerie`
- `babydoll`
- `chemise`
- `teddy`
- `bodystocking`
- `garter_belt`
- `garter_straps`
- `corset`
- `bustier`
- `camisole_(underwear)`
- `slip_(clothing)`
- `fundoshi`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsBuild` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
