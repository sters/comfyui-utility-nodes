# Tags: Decorate

`UtilityNodes/TagMaster` menu tree. Prefixes tags in a bundle that belong to a chosen category with a decoration phrase built from a second bundle. Use it to attach colors / patterns / materials to a specific layer of an upstream preset or tag-toggle node without rewriting the tag itself.

## Inputs

- `separator` (STRING).
- `target_category` (COMBO): pick the category whose tags should be decorated. The list is populated from every `TagNodeBase` subclass registered in this pack — e.g. `clothing.bottoms`, `clothing.legwear`, `clothing.headwear`, `body.hair.color`, ... `(none)` is a no-op (pass-through).
- `bundle` (CUUN_TAGS, optional): the main bundle to decorate. Typically the output of `TagsMerge`.
- `decoration` (CUUN_TAGS, optional): bundle whose tags are joined with spaces and used as the prefix. Underscores become spaces (`light_blue` → `light blue`).

Both `bundle` and `decoration` accept a list, and `TagDecorate` takes the **Cartesian product** internally (see "Variant generation" below).

## Outputs (lists, `OUTPUT_IS_LIST=True`)

- `warnings` (STRING list): per-pair warnings — "no tags matched target_category" or "decoration provided but no category selected".
- `bundle` (CUUN_TAGS list): per-pair decorated bundle, feed into another `TagDecorate` or `TagsMerge` to multiply variants further. One flattened prompt per (bundle × decoration) pair also previews as the node's OUTPUT_NODE preview.

## Variant generation

`INPUT_IS_LIST=True` wraps scalar inputs in a 1-element list, so both inputs are uniformly treated as axes:

| `bundle` | `decoration` | output count | typical use |
|---|---|---|---|
| 1 bundle | 1 decoration | 1 | "fix the skirt to red plaid" |
| 1 bundle | N decorations (from `TagsExplode`) | N | "vary the skirt colour over N choices" |
| M bundles | 1 decoration | M | "apply the same red plaid to each top variant" |
| M bundles | N decorations | M × N | "every top × every colour" |

Chaining two `TagDecorate`s multiplies axes:
`Decorate(skirt, [red,green,blue])` → 3 bundles → `Decorate(tops, [shirt,blouse,hoodie])` → 3 × 3 = 9 prompts.

## How decoration is matched

`TagDecorate` looks up each tag in the main bundle against a global tag→category registry built at import time from every `TagNodeBase` subclass's `TAGS`. Tags from `CharacterPreset` (which emit their own `preset.character` category) are still resolved correctly because the registry knows that, e.g., `pleated_skirt` originated in `ClothingBottoms` regardless of which node placed it in the bundle.

The `extra` selection is always passed through untouched.

## Decoration sources

Any `CUUN_TAGS` bundle works as `decoration`. The natural fits in this pack:

- **`ColorPalette`** (`Decoration: Color Palette`) — bare colors like `red`, `green`, `light_blue`.
- **`ClothingPattern`** — `plaid`, `checkered`, `floral_print`, ...
- **`ClothingMaterial`** — `silk`, `lace`, `denim`, ...

Merge multiple decoration sources through `TagsMerge` before wiring into `decoration`.

## Example: red and green plaid skirt on a school-uniform preset

```
CharacterPreset(serafuku_schoolgirl) ─┐
                                      ├─► TagsMerge ─► TagDecorate ─► prompt
[other nodes...]                    ──┘                ▲ target_category: clothing.bottoms
                                                       │
ColorPalette(red, green) ─┐                            │
                          ├─► TagsMerge ───────────────┘ decoration
ClothingPattern(plaid)  ──┘
```

`pleated_skirt` becomes `red green plaid pleated skirt` in the output; the rest of the preset (hair, top, footwear) is untouched. Chain another `TagDecorate` after this one to decorate a different category in the same workflow.

## Notes

- For a category miss, the bundle is returned unchanged and a warning is logged. The decoration phrase is dropped (never injected as a free-floating tag).
- The decorated tag is rewritten with spaces (`pleated_skirt` → `red green plaid pleated skirt`). SD models handle both forms; the spaced form reads more naturally inside the longer phrase.
