# Tags Combinator (axes × bundles)

`utility/text` category. Cartesian product over up to 8 axes of `CUUN_TAGS` bundles. Each axis is a list of bundles; each combination is resolved through `TagsMerge` and emitted as a STRING list, ready for downstream `CLIPTextEncode` / `KSampler` / `SaveImage` to iterate over.

## Inputs

- `separator` (STRING): joiner inside each generated prompt.
- `axis_1` ... `axis_8` (CUUN_TAGS, optional, `INPUT_IS_LIST=True`): each axis takes a **list of bundles**. Wire either:
  - A single preset → 1 value on this axis.
  - A tag-toggle node through `TagsExplode` → one value per checked tag.
  - Multiple bundles concatenated upstream → manual axis values.

Unwired / empty axes are skipped (they don't zero out the product).

## Outputs (all lists, `OUTPUT_IS_LIST=True`)

- `prompt` (STRING): one resolved prompt per combination.
- `label` (STRING): per-combination identifier, joined with `__`. Per-axis segment is:
  - Single-tag bundle → the tag itself (e.g. `red_hair`)
  - Multi-tag bundle with dotted category (preset) → the suffix after the last dot (e.g. `serafuku_schoolgirl` from `character.serafuku_schoolgirl`)
  - Multi-tag bundle without dotted category → first tag
- `index` (INT): 0-based counter.
- `warnings` (STRING): `TagsMerge` warnings per combination — useful for debugging unexpected drops.

## Axis order = priority

`TagsMerge`'s MUTEX_GROUPS is **last-wins**, so axis order determines priority:

- `axis_1` is the base / fixed bundle (its mutex-group tags get overridden by later axes)
- `axis_8` has the highest override priority

For the canonical "preset + overrides" pattern:

```
axis_1 = CharacterPreset(serafuku_schoolgirl)
axis_2 = HairColor(red, blue, green, black)   ─→ TagsExplode
axis_3 = BodyFigure(muscular, slim, curvy, plump)  ─→ TagsExplode
axis_4 = BreastsSize(flat, small, medium, large)   ─→ TagsExplode
```

→ 1 × 4 × 4 × 4 = **64 prompts**. The preset's `brown_hair` gets overridden by each axis_2 hair color; the preset's clothing (`serafuku`, `pleated_skirt`, ...) is preserved since it doesn't conflict with the override axes.

## Notes

- `TAG_CONFLICTS` (hard semantic guards like `nude` dropping clothing) still apply per combination and aren't order-sensitive. If `axis_1` is an NSFW scene preset containing `nude` and `axis_2` is a clothing tag, the clothing gets dropped regardless of order. Pick a different base if you need clothing in the output.
- The `warnings` output is the easiest way to diagnose "why did my tag vanish" — read one row to see what `TagsMerge` decided.
