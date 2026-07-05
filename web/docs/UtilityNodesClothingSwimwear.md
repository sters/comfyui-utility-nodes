# Clothing: Swimwear

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
**Mutex node** — only one of the toggled tags survives after `TagsBuild`.
Internal layer / category: `clothing` / `clothing.swimwear`.

## Inputs

- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsBuild` (carries category + mutex metadata).

## Tags

- `swimsuit`
- `one-piece_swimsuit`
- `school_swimsuit`
- `competition_swimsuit`
- `bikini`
- `string_bikini`
- `side-tie_bikini`
- `front-tie_bikini`
- `micro_bikini`
- `sling_bikini`
- `halterneck_bikini`
- `frilled_bikini`
- `polka_dot_bikini`
- `striped_bikini`
- `o-ring_bikini`
- `bikini_top`
- `bikini_bottom`
- `swim_briefs`
- `swim_trunks`
- `rash_guard`
- `wetsuit`
- `highleg_swimsuit`
- `thong_bikini`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsBuild` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
