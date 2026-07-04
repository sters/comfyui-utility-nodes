# Tags: Merge & Validate

`UtilityNodes/TagMaster` menu tree. The pipeline's terminal **build** step: accepts up to 10 `CUUN_TAGS` bundles from tag-toggle nodes/presets, plus up to 10 `CUUN_TAG_SPEC` specs from [Random Pick](UtilityNodesTagsRandomPick.md) / [Random Bundle](UtilityNodesTagsRandomBundle.md), resolves cross-node conflicts (and any random specs), and emits a final STRING.

## Inputs

- `separator` (STRING).
- `bundle_1` ... `bundle_10` (CUUN_TAGS, optional): wire each tag node's `bundle` output here.
- `spec_1` ... `spec_10` (CUUN_TAG_SPEC, optional): wire `TagsRandomPick` / `TagsRandomBundle`'s `spec` output here. Resolved with each spec's own `seed` before conflict resolution runs.
- `extra` (STRING, multiline, optional): appended verbatim after the resolved tags. Never dropped by conflict rules.

## Outputs

- `prompt` (STRING): final prompt.
- `warnings` (STRING): log of every tag dropped during resolution. Useful for debugging "why did my tag vanish?".
- `bundle` (CUUN_TAGS): the resolved bundle. Re-routable into another `TagsMerge` if you want to layer.

## Resolution order

0. **Spec resolution**: every wired `spec_i` is resolved first (`tag_pick` samples its pool, `bundle_choice` picks one candidate), each using its own `seed`. The resulting selections are appended after the `bundle_i` selections, in spec input order, then resolution proceeds exactly as below.
1. **`mutex_within`**: for selections that declare themselves mutex (e.g. `HairColor`), keep only the first selection per category, and only the first tag inside it. So wiring two `HairColor` nodes drops the second; checking every box on a mutex node still keeps only the leading tag.
2. **`MUTEX_GROUPS`** (in `nodes/tags/_conflicts.py`): cross-category sets where at most one member may survive. E.g. `long_hair` vs `short_hair` from different nodes — **last occurrence in input order wins**, so later bundles override earlier ones (preset's `brown_hair` is overwritten by a later explicit `red_hair`).
3. **`TAG_CONFLICTS`**: trigger → suppressed-tags map. If a trigger tag appears anywhere in the bundle, the listed tags are dropped from every non-`extra` selection. The trigger itself is never dropped. Examples:
   - `nude` / `completely_nude` → all clothing tags
   - `topless` → tops + bras + corset/bustier + full-body underwear + dresses (panties / garter belt are kept)
   - `bottomless` → bottoms + all panties + full-body underwear + dresses (bras are kept)
   - `barefoot` → footwear + legwear (legwear covers the feet, so it's removed too)
   - `no_shoes` → footwear only (`thighhighs` survives)
   - `no_panties` → panty styles only (bras / corsets survive)
   - `no_bra` → bra styles only
4. Surviving tags are flattened in input order, `extra` is appended, and the result is joined with `separator`.

## Tips

- For consistent prompts, route **every tag node's bundle** through one `TagsMerge` rather than concatenating their `prompt` outputs with `TextConcat` — only the merge path enforces the conflict rules.
- Read `warnings` once to confirm the resolution did what you expected; many silent drops can hide a wiring mistake.
