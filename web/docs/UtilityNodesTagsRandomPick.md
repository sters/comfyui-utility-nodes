# Tags: Random Pick

`UtilityNodes/TagMaster` menu tree. Describes a random sample of `count` tags out of a CUUN_TAGS bundle — the actual pick is deferred to [Merge & Validate](UtilityNodesTagsMerge.md), the pipeline's terminal build step. Use for "give me a random subset of these tags in the prompt" — variety without writing a separate template for each combination.

## Inputs

- `count` (INT, ≥ 1): number of tags to sample (without replacement).
- `seed` (INT): RNG seed. Same seed = same picks.
- `bundle` (CUUN_TAGS, optional).

## Outputs

- `spec` (CUUN_TAG_SPEC): an unresolved `tag_pick` spec carrying `count`, `seed`, and the bundle to sample from. Wire it into one of [Merge & Validate](UtilityNodesTagsMerge.md)'s `spec_i` inputs to resolve it.

## Behavior

- No randomness happens in this node — it only packages its inputs into a spec. [Merge & Validate](UtilityNodesTagsMerge.md) does the actual sampling.
- On resolution: tags from every non-`extra` selection are flattened into one pool before sampling. Category metadata of the source selections is lost on purpose — the picked tags live under a new `random_pick` category.
- If `count >= number of available tags`, every tag is returned (shuffled).
- `extra` selections pass through untouched.

## Typical use

Combine with a tag-toggle node to express "vary one of these N options each run":

```
ClothingPattern(plaid, checkered, polka_dot, floral_print) ─► TagsRandomPick(count=1, seed=…) ─► TagsMerge.spec_1
                                                                                                       │
                                                                                                       ▼
                                                                                          one random pattern per run
```

For deterministic per-image variation, wire the KSampler seed (or any other changing INT) into the `seed` input.
