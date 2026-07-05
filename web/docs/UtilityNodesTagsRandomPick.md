# Tags: Random Pick

`UtilityNodes/TagMaster` menu tree. Describes a random sample of `count` tags out of a resolved CUUN_TAGS bundle — the actual pick is deferred to [Merge & Validate](UtilityNodesTagsMerge.md) (or a [Combinator](UtilityNodesTagsCombinator.md) / [Build from Rules](UtilityNodesTagsBuildFromRules.md) `axis_i`), the places that resolve specs. Use for "give me a random subset of these tags in the prompt" — variety without writing a separate template for each combination.

## Inputs

- `count` (INT, ≥ 1): number of tags to sample (without replacement).
- `bundle` (CUUN_TAGS, optional): must already be resolved (a plain tag node's output, not another unresolved spec).

This node has **no `seed` input** — the only seed in the pipeline lives on [Merge & Validate](UtilityNodesTagsMerge.md) (the actual build step), which XOR-mixes it with each spec's own slot index when resolving.

## Outputs

- `spec` (CUUN_TAG_SPEC — the same socket type as `CUUN_TAGS`): an unresolved `tag_pick` spec carrying `count` and the bundle to sample from. Wire it into one of [Merge & Validate](UtilityNodesTagsMerge.md)'s `bundle_i` inputs to resolve it immediately, or into a [Combinator](UtilityNodesTagsCombinator.md)/[Build from Rules](UtilityNodesTagsBuildFromRules.md) `axis_i` to make it a *deferred axis* — not cross-multiplied, resolved once independently per combination.

## Behavior

- No randomness happens in this node — it only packages its inputs into a spec. Resolution (sampling) happens wherever the spec ends up, using whichever seed the resolving node owns.
- On resolution: tags from every non-`extra` selection are flattened into one pool before sampling. Category metadata of the source selections is lost on purpose — the picked tags live under a new `random_pick` category.
- If `count >= number of available tags`, every tag is returned (shuffled).
- `extra` selections pass through untouched.

## Typical use

Combine with a tag-toggle node to express "vary one of these N options each run":

```
ClothingPattern(plaid, checkered, polka_dot, floral_print) ─► TagsRandomPick(count=1) ─► TagsMerge.bundle_1 (seed=…)
                                                                                                       │
                                                                                                       ▼
                                                                                          one random pattern per run
```

For deterministic per-image variation, wire the KSampler seed (or any other changing INT) into `TagsMerge`'s `seed` input.
