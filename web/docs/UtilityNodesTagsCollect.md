# Tags: Collect (whole-bundle axis)

`UtilityNodes/TagMaster` menu tree. Gathers several whole `CUUN_TAGS` bundles into a **list of bundles**, one element per wired input, each kept intact. Designed as the adapter that turns "N alternative bundles" (e.g. several `CharacterPreset`s) into a single axis for `TagsCombinator` — one combination per bundle, with no flattening or per-tag explosion.

## Inputs

- `bundle_1` ... `bundle_10` (CUUN_TAGS, optional): each wired bundle becomes one element of the output list. Unwired / empty inputs are skipped.

## Outputs

- `bundles` (CUUN_TAGS list, `OUTPUT_IS_LIST=True`): the wired bundles, in input order, each preserved whole.

## Why not `TagsMerge` → `TagsExplode`?

To vary over multiple characters you might reach for:

```
Merge(Character(blazer), Character(serafuku)) ─→ Explode ─→ Combinator
```

This does **not** do what you want: `TagsMerge` flattens both characters into one bundle (resolving conflicts between them), then `TagsExplode` re-splits that bundle **per tag** — so you get a combinatorial blow-up of individual tags, not one row per character.

`TagsCollect` is the right primitive — it keeps each character as one discrete axis value:

```
Collect(Character(blazer), Character(serafuku)) ─→ Combinator.axis_1
```

→ 2 combinations: one full `blazer_schoolgirl`, one full `serafuku_schoolgirl`.

## Relationship to `TagsExplode`

- `TagsExplode`: **one** bundle → list of **per-tag** bundles (vary over the tags inside a node).
- `TagsCollect`: **several** bundles → list of **whole** bundles (vary over the bundles themselves).

Both produce a `CUUN_TAGS` list ready to wire into a `TagsCombinator` axis.
