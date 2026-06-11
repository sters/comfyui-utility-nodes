# Tags: Random Bundle

`UtilityNodes/TagMaster` menu tree. Picks **one whole CUUN_TAGS bundle** at random out of several wired alternatives and returns it intact. The bundle-level counterpart to [Random Pick](UtilityNodesTagsRandomPick.md): Random Pick samples *tags* out of one bundle's flattened pool; Random Bundle treats each wired input as one indivisible candidate and returns exactly one of them, with categories / layers / `mutex_within` preserved.

## Inputs

- `seed` (INT): RNG seed. Same seed = same choice. Set `control_after_generate` to `randomize` to re-roll every run.
- `bundle_1` … `bundle_10` (CUUN_TAGS, optional): the candidate bundles. Unwired or empty inputs are ignored.

## Outputs

- `bundle` (CUUN_TAGS): one of the wired inputs, returned unchanged. If nothing is wired, an empty bundle.

## Behavior

- Selection is uniform over the non-empty wired inputs.
- The chosen bundle is passed through untouched — no flattening, no category loss, no merging.
- This is the node for "pick one of these N alternatives each run". Do **not** feed a [Collect](UtilityNodesTagsCollect.md) list into [Random Pick](UtilityNodesTagsRandomPick.md) for this — Random Pick does not consume a list, so ComfyUI broadcasts it per element and keeps every candidate. Random Bundle takes the candidates as discrete inputs and collapses them to one.

## Typical use

Random-one-per-run prompts need no [Combinator](UtilityNodesTagsCombinator.md) / [Select](UtilityNodesTagsSelect.md): each axis emits one bundle, and a final [Merge & Validate](UtilityNodesTagsMerge.md) combines them.

```
CharacterPreset A ─┐
CharacterPreset B ─┤
CharacterPreset C ─┼─► TagsRandomBundle(seed=…, randomize) ─► one random character per run
CharacterPreset D ─┘
```

Pair the two random primitives by axis shape:

- **one random *tag* from a node** → `TagsRandomPick(count=1)`
- **one random *whole bundle* from alternatives** → `TagsRandomBundle`

For deterministic per-image variation, wire the KSampler seed (or any changing INT) into `seed`.
