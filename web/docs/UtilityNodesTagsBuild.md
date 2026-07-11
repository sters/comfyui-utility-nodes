# Tags: Build

`UtilityNodes/TagMaster` menu tree. The pipeline's terminal **build** step: accepts a single `CUUN_TAGS` bundle — either already-resolved (from a tag-toggle node, a preset, a [Concat](UtilityNodesTagsConcat.md) merge of several, or a [Combinator](UtilityNodesTagsCombinator.md) / [Build from Rules](UtilityNodesTagsBuildFromRules.md) combo with no deferred axis) or still-unresolved (from [Random Pick](UtilityNodesTagsRandomPick.md) / [Random Bundle](UtilityNodesTagsRandomBundle.md), or a Combinator/Build from Rules combo that folded one in) — resolves conflicts (and the bundle itself, if unresolved), and emits a final STRING. To merge several tag sources into one bundle first, use `TagsConcat` (or `TagsCombinator` for combinatorial expansion) upstream.

## Inputs

- `separator` (STRING).
- `seed` (INT): the **only** seed in the whole tag pipeline — `TagsRandomPick`/`TagsRandomBundle` carry none of their own. Mixed into the bundle before resolving if it's unresolved.
- `bundle` (CUUN_TAGS, optional): wire any tag node's `bundle` output here — resolved or unresolved, or a `TagsConcat`/`TagsCombinator` merge of several — they all ride the same socket.
- `extra` (STRING, multiline, optional): appended verbatim after the resolved tags. Never dropped by conflict rules.

## Outputs

- `prompt` (STRING): final prompt.
- `warnings` (STRING): log of every tag dropped during resolution. Useful for debugging "why did my tag vanish?".
- `bundle` (CUUN_TAGS): the resolved bundle. Re-routable into another `TagsBuild` if you want to layer.

## Resolution order

0. **Unresolved-input resolution**: if the wired bundle isn't already resolved, it's resolved first (`TagsRandomPick`'s "pick `count`" samples its pool, `TagsRandomBundle`'s "pick one" picks one candidate — itself resolved further if that candidate wasn't fixed either — a `composite` Spec resolves each of its children independently and concatenates them), using `seed`. Resolution then proceeds exactly as below.
1. **`mutex_within`**: for selections that declare themselves mutex (e.g. `HairColor`), keep only the first selection per category, and only the first tag inside it. So a merged bundle carrying two `HairColor` selections drops the second; checking every box on a mutex node still keeps only the leading tag.
2. **`MUTEX_GROUPS`** (in `nodes/tags/_conflicts.py`): cross-category sets where at most one member may survive. E.g. `long_hair` vs `short_hair` from different nodes — **last occurrence in input order wins**, so later selections override earlier ones (preset's `brown_hair` is overwritten by a later explicit `red_hair`).
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

- To combine several tag nodes into one prompt, merge their bundles with `TagsConcat` first, then wire the result into `TagsBuild`'s single `bundle` input — rather than concatenating their `prompt` outputs with `TextConcat`, which skips conflict resolution entirely.
- Read `warnings` once to confirm the resolution did what you expected; many silent drops can hide a wiring mistake.
