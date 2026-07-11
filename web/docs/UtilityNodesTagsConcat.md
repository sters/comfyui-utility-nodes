# Tags: Concat

`UtilityNodes/TagMaster` menu tree. Concatenates several `CUUN_TAGS` bundles into **one bundle**, verbatim — every selection from every wired input, kept exactly as-is, in input order. No mutex/conflict resolution happens here.

## Inputs

- `bundle_1` ... `bundle_10` (CUUN_TAGS, optional): resolved or unresolved, either is fine. Unwired inputs are skipped.

## Outputs

- `bundle` (CUUN_TAGS): if every wired input was already resolved, one `kind="fixed"` bundle. If any input was still unresolved (a `TagsRandomPick`/`TagsRandomBundle` output, or another unresolved combo), a `kind="composite"` Spec carrying every input through untouched, in order — resolving it later (typically via `TagsBuild`) resolves each child independently and flattens them together.

## Why not `TagsBuild`?

`TagsBuild` can also combine several bundles into one (via its own single `bundle` input), but it always applies `MUTEX_GROUPS` / `TAG_CONFLICTS` first. That's correct when you want the final, validated prompt — but wrong when you just want the raw combined *candidate pool* for something else to pick from later, since conflict resolution could silently drop a candidate before it ever gets a chance to be picked.

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

Note `TagsRandomPick`'s own `bundle` input still requires an already-resolved pool to sample from — wiring a `TagsConcat` that included an unresolved input (so its output is `composite`, not `fixed`) straight into `TagsRandomPick` raises. That combination belongs on a plain `TagsBuild` instead (merge several tag sources — some fixed, one still-random — into one bundle first with `TagsConcat`, then resolve everything through `TagsBuild`).

## Relationship to other combining nodes

- `TagsConcat`: several bundles (fixed or not) → **one** bundle, no conflict resolution (this node).
- `TagsCollect`: several bundles → a **list** of whole bundles, one axis value per input (for `TagsCombinator`).
- `TagsBuild`: a single bundle (merge several with `TagsConcat` first if needed) → **one** resolved bundle, *with* mutex/conflict resolution and a final `prompt` STRING.
