# Tags: Filter (drop category)

`UtilityNodes/TagMaster` menu tree. Drops every tag in a `CUUN_TAGS` bundle whose **registered category** matches `target_category`. Use to subtract a single aspect from a preset (e.g. keep `serafuku_schoolgirl` but drop the legwear) without rebuilding the preset by hand.

## Inputs

- `target_category` (combo): a category from the global tag registry, or `(none)` to pass through unchanged.
- `bundle` (CUUN_TAGS, optional): input bundle. If unwired, output is empty.

## Outputs

- `bundle` (CUUN_TAGS): same selections as input, with matching tags removed. Selections that lose every tag are dropped entirely; `mutex_within` / `layer` / `category` metadata is preserved on what remains. The filtered prompt also previews as the node's OUTPUT_NODE preview.

## Behavior

- Category lookup uses `TAG_CATEGORY_REGISTRY` — the same per-tag registry `TagsDecorate` uses — **not** the selection's own `category` field. That way preset selections (which use a `preset.X` selection-category) still have their inner tags filtered by the tag's original category.
- Tags in the `extra` selection always pass through (they're free-form text and aren't in the registry).
- Unregistered tags (free-form additions) are kept even if the selection they live in carries the targeted category, since the registry has no record of their intent.
- Chain multiple `TagsFilter` nodes to drop more than one category.

## Typical wiring

```
CharacterPreset(serafuku_schoolgirl) ─► TagsFilter(clothing.legwear) ─► …
# result: long_hair, black_hair, bangs, hair_ribbon, serafuku,
#         sailor_collar, pleated_skirt, loafers
```

To swap the dropped aspect for your own choice, feed the result and a fresh source node into `TagsMerge`:

```
CharacterPreset ─► TagsFilter(clothing.legwear) ─┐
ClothingLegwear(bare_legs)                     ─┼─► TagsMerge
```
