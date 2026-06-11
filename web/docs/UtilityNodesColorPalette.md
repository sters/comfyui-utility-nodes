# Decoration: Color Palette

`UtilityNodes/TagMaster` menu tree. Emits bare color names (`red`, `green`, `light_blue`, ...) as a `CUUN_TAGS` bundle. Intended as a `decoration` input for `TagsDecorate`.

## Inputs

- `invert` (BOOLEAN): if `True`, every checkbox is flipped.
- One BOOLEAN per color. Default is off.
- `extra` (STRING, multiline, optional).

## Outputs

- `bundle` (CUUN_TAGS): `category = decoration.color`, `layer = decoration`.

## Why a separate node

`HairColor` / `EyesColor` etc. emit fully-formed tags like `red_hair` — useful as standalone tags but unwanted as a prefix on something like `pleated_skirt`. `ColorPalette` exists to provide the bare color names that read cleanly when prefixed to another tag.

## Example wiring

```
ColorPalette(red, green) ─┐
                          ├─► TagsMerge ─► TagsDecorate.decoration
ClothingPattern(plaid)  ──┘                 ▲ target_category: clothing.bottoms
                                            │
[preset / clothing nodes] ─► TagsMerge ─────┘ bundle
```

The downstream `pleated_skirt` becomes `red green plaid pleated skirt`. See `TagsDecorate` for the full pipeline.

## Tips

- Don't wire `ColorPalette` directly into the main `TagsMerge` — the bare colors will appear as standalone tags in your prompt. Route it through `TagsDecorate`'s `decoration` input.
