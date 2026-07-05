# Tags: Random Bundle

`UtilityNodes/TagMaster` menu tree. Describes a choice of **one whole resolved CUUN_TAGS bundle** out of several wired alternatives — the actual choice is deferred to [Build](UtilityNodesTagsBuild.md) (or a [Combinator](UtilityNodesTagsCombinator.md) / [Build from Rules](UtilityNodesTagsBuildFromRules.md) `axis_i`), which resolves it intact. The bundle-level counterpart to [Random Pick](UtilityNodesTagsRandomPick.md): Random Pick samples *tags* out of one bundle's flattened pool; Random Bundle treats each wired input as one indivisible candidate and resolves to exactly one of them, with categories / layers / `mutex_within` preserved.

## Inputs

- `bundle_1` … `bundle_10` (CUUN_TAGS, optional): the candidate bundles — each must already be resolved. Unwired or empty inputs are ignored.

This node has **no `seed` input** — the only seed in the pipeline lives on [Build](UtilityNodesTagsBuild.md) (the actual build step), which XOR-mixes it with this node's own output's slot index when resolving. Set `control_after_generate` to `randomize` on `TagsBuild`'s `seed` to re-roll every run.

## Outputs

- `bundle` (CUUN_TAGS): an unresolved "pick one of these" bundle carrying the candidates. Wire it into one of [Build](UtilityNodesTagsBuild.md)'s `bundle_i` inputs to resolve it immediately, or into a [Combinator](UtilityNodesTagsCombinator.md)/[Build from Rules](UtilityNodesTagsBuildFromRules.md) `axis_i` to make it a *deferred axis* — not cross-multiplied, resolved once independently per combination.

## Behavior

- No randomness happens in this node — it only packages the wired candidates. Resolution (the actual choosing) happens wherever the output ends up, using whichever seed the resolving node owns, uniformly over the non-empty wired inputs.
- The chosen bundle's selections are merged like any other input — no flattening or category loss, but it does go through the same mutex/conflict resolution as everything else once wired in.
- This is the node for "pick one of these N alternatives each run". Do **not** feed a [Collect](UtilityNodesTagsCollect.md) list into [Random Pick](UtilityNodesTagsRandomPick.md) for this — Random Pick does not consume a list, so ComfyUI broadcasts it per element and keeps every candidate. Random Bundle takes the candidates as discrete inputs and collapses them to one.

## Typical use

Random-one-per-run prompts need no [Combinator](UtilityNodesTagsCombinator.md) / [Select](UtilityNodesTagsSelect.md): each axis emits one bundle (resolved or not), and a final [Build](UtilityNodesTagsBuild.md) combines them.

```
CharacterPreset A ─┐
CharacterPreset B ─┤
CharacterPreset C ─┼─► TagsRandomBundle() ─► TagsBuild.bundle_1 (seed=…, randomize) ─► one random character per run
CharacterPreset D ─┘
```

Pair the two random primitives by axis shape:

- **one random *tag* from a node** → `TagsRandomPick(count=1)`
- **one random *whole bundle* from alternatives** → `TagsRandomBundle`

For deterministic per-image variation, wire the KSampler seed (or any changing INT) into `TagsBuild`'s `seed`.
