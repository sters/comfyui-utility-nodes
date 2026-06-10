# Tags Combinator (axes × bundles)

`UtilityNodes/TagMaster` menu tree. Cartesian product over up to 8 axes of `CUUN_TAGS` bundles. Each axis is a list of bundles; each combination is emitted as a **concatenated `CUUN_TAGS` bundle**. The combinator does **not** merge or resolve conflicts itself — wire its `bundle` output into a `TagsMerge` ("Merge & Validate") node, which ComfyUI broadcasts over the list to validate and flatten one prompt per combination.

## Inputs

- `axis_1` ... `axis_8` (CUUN_TAGS, optional, `INPUT_IS_LIST=True`): each axis takes a **list of bundles**. Wire either:
  - A single preset → 1 value on this axis.
  - A tag-toggle node through `TagsExplode` → one value per checked tag.
  - Several whole bundles through `TagsCollect` → one value per bundle (e.g. multiple characters).

Unwired / empty axes are skipped (they don't zero out the product).

## Outputs (all lists, `OUTPUT_IS_LIST=True`)

- `bundle` (CUUN_TAGS): one concatenated bundle per combination — the chosen axis bundles joined in axis order, **unmerged**. Feed into `TagsMerge` for conflict resolution and the final prompt string.
- `label` (STRING): per-combination identifier, joined with `__`. Per-axis segment is:
  - Single-tag bundle → the tag itself (e.g. `red_hair`)
  - Multi-tag bundle with dotted category (preset) → the suffix after the last dot (e.g. `serafuku_schoolgirl` from `character.serafuku_schoolgirl`)
  - Multi-tag bundle without dotted category → first tag
- `index` (INT): 0-based counter.

## Wiring

```
Combinator.bundle ─→ TagsMerge.bundle_1 ─→ (prompt) ─→ CLIPTextEncode ─→ KSampler ─→ SaveImage
                       (broadcast per combination; emits prompt + warnings lists)
```

`TagsMerge` is not `INPUT_IS_LIST`, so ComfyUI runs it once per combination in the list and produces aligned `prompt` / `warnings` lists. The combinator's `label` / `index` outputs stay aligned alongside (useful for `SaveImage` filename prefixes).

## Axis order = priority

`TagsMerge`'s MUTEX_GROUPS is **last-wins**, so axis order determines priority once merged:

- `axis_1` is the base / fixed bundle (its mutex-group tags get overridden by later axes)
- `axis_8` has the highest override priority

For the canonical "preset + overrides" pattern:

```
axis_1 = CharacterPreset(serafuku_schoolgirl)
axis_2 = HairColor(red, blue, green, black)   ─→ TagsExplode
axis_3 = BodyFigure(muscular, slim, curvy, plump)  ─→ TagsExplode
axis_4 = BreastsSize(flat, small, medium, large)   ─→ TagsExplode
```

→ 1 × 4 × 4 × 4 = **64 bundles** → `TagsMerge` → 64 prompts. The preset's `brown_hair` gets overridden by each axis_2 hair color; the preset's clothing (`serafuku`, `pleated_skirt`, ...) is preserved since it doesn't conflict with the override axes.

To vary over multiple **whole characters** (not their individual tags), put them on one axis through `TagsCollect`:

```
axis_1 = Collect(Character(blazer), Character(serafuku))   → 2 combinations, one per character
```

## Large sweeps — mind the memory

The list output fans **all** combinations out in a single Run, and ComfyUI materialises the whole list at each pipeline stage (N decoded images **and** N detailer outputs in memory at once). Model weights (VRAM) are reused across iterations and stay constant, but the accumulated intermediate **tensors** (system RAM) overflow at large N (e.g. 3 × 10 × 10 = 300).

For big sweeps, switch to "N Runs, 1-wide" with `TagsSelect`: wire `bundle` / `label` into it, drive `index` from an incrementing `Seed`, and queue the prompt N times. Each Run resolves to one combination, so peak memory stays at one image's worth and progress is saved incrementally.

## Notes

- `TAG_CONFLICTS` (hard semantic guards like `nude` dropping clothing) and MUTEX_GROUPS are applied by the downstream `TagsMerge`, per combination, exactly as for any other bundle.
- The `warnings` output now lives on `TagsMerge`, not the combinator — read one row to diagnose "why did my tag vanish".
