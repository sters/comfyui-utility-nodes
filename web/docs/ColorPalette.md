# Decoration: Color Palette

`utility/text` category. Emits bare color names (`red`, `green`, `light_blue`, ...) as a `CUUN_TAGS` bundle. Intended as a `decoration` input for `TagDecorate`.

## Inputs

- `separator` (STRING).
- `preset` (combo): `custom` / `all_on` / `all_off` / `invert`.
- One BOOLEAN per color. Default is off.
- `extra` (STRING, multiline, optional).

## Outputs

- `prompt` (STRING).
- `bundle` (CUUN_TAGS): `category = decoration.color`, `layer = decoration`.

## Why a separate node

`HairColor` / `EyesColor` etc. emit fully-formed Danbooru tags like `red_hair` — useful as standalone tags but unwanted as a prefix on something like `pleated_skirt`. `ColorPalette` exists to provide the bare color names that read cleanly when prefixed to another tag.

## Example wiring

```
ColorPalette(red, green) ─┐
                          ├─► TagsMerge ─► TagDecorate.decoration
ClothingPattern(plaid)  ──┘                 ▲ target_category: clothing.bottoms
                                            │
[preset / clothing nodes] ─► TagsMerge ─────┘ bundle
```

The downstream `pleated_skirt` becomes `red green plaid pleated skirt`. See `TagDecorate` for the full pipeline.

## Tips

- Don't wire `ColorPalette` directly into the main `TagsMerge` — the bare colors will appear as standalone tags in your prompt. Route it through `TagDecorate`'s `decoration` input.
