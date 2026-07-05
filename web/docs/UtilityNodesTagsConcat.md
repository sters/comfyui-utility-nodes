# Tags: Concat

`UtilityNodes/TagMaster` menu tree. Concatenates several whole resolved `CUUN_TAGS` bundles into **one bundle**, verbatim — every selection from every wired input, kept exactly as-is, just appended in input order. No mutex/conflict resolution happens here.

## Inputs

- `bundle_1` ... `bundle_10` (CUUN_TAGS, optional): must already be resolved. Unwired inputs are skipped.

## Outputs

- `bundle` (CUUN_TAGS): the concatenated result as one `kind="fixed"` bundle.

## Why not `TagsBuild`?

`TagsBuild` can also combine several bundles into one, but it always applies `MUTEX_GROUPS` / `TAG_CONFLICTS` first. That's correct when you want the final, validated prompt — but wrong when you just want the raw combined *candidate pool* for something else to pick from later, since conflict resolution could silently drop a candidate before it ever gets a chance to be picked.

The motivating case: pick **one** tag out of the union of two nodes' tags, e.g. "one of everything checked on `SceneIndoor` **and** `SceneOutdoor` combined":

```
SceneIndoor  ─┐
              ├─→ TagsConcat(bundle_1, bundle_2) ─→ bundle
SceneOutdoor ─┘
                        │
                        ▼
              TagsRandomPick(count=1, bundle=…)
```

Routing that combined pool through `TagsBuild` instead would resolve any cross-node conflicts *before* the random pick even happens, which isn't what you want when the whole point is to let the pick choose freely from every option.

## Relationship to other combining nodes

- `TagsConcat`: several bundles → **one** flattened bundle, no conflict resolution (this node).
- `TagsCollect`: several bundles → a **list** of whole bundles, one axis value per input (for `TagsCombinator`).
- `TagsBuild`: several bundles (or unresolved ones) → **one** resolved bundle, *with* mutex/conflict resolution and a final `prompt` STRING.
