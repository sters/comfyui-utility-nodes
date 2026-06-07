# Workflow templates

JSON files in this directory are picked up by ComfyUI's [Workflow
Templates](https://docs.comfy.org/custom-nodes/workflow_templates)
feature and surfaced under **Workflow → Browse Templates → comfyui-utility-nodes**.

## Templates

### `character_pipeline.json`

End-to-end text-to-image graph that demonstrates the recommended
positive-prompt pipeline:

```
CharacterPreset(miko) ─┐
PersonalityPreset(genki) ─┤
SituationPreset(shrine_visit) ─┼─► TagsMerge ─► CLIPTextEncode (positive)
MetaQuality(all_on) ─┘
                                                         │
BadGeneral(all_on) ──────────► CLIPTextEncode (negative) │
                                                         │
CheckpointLoader ─┬─► MODEL ────────────────────────────►│ KSampler ─► VAEDecode ─► PreviewImage
                  ├─► CLIP (both encoders)               │
                  └─► VAE ──────────────────────────────►│
EmptyLatentImage(512×512×1) ────────────────────────────►│
```

After loading the template:

- **Replace the model name** on `CheckpointLoaderSimple` — the default
  (`SD1.5/fantexiRealistic_v10.safetensors`) is a placeholder borrowed
  from [Impact-Pack's FaceDetailer example](https://github.com/ltdrdata/ComfyUI-Impact-Pack/blob/Main/example_workflows/1-FaceDetailer.json).
- Tweak the preset combos (`CharacterPreset` / `PersonalityPreset` /
  `SituationPreset`) to taste — `TagsMerge` resolves any conflicts.
- KSampler defaults: seed=42, steps=20, cfg=8, sampler=euler,
  scheduler=normal, denoise=1.0 (also borrowed from the FaceDetailer
  reference).

### `decorate_schoolgirl_skirt.json`

Demonstrates **chained `TagDecorate`** for true multi-axis variant
generation. Two decoration stages multiply axes inside ComfyUI's
graph, producing a 3 × 3 = 9-prompt sweep with one click.

```
CharacterPreset(serafuku_schoolgirl) ─► TagsMerge ─┐
                                                   │
ColorPalette(red, green, blue) ─► TagsExplode ─────┤   (skirt color axis)
                                                   ▼
                                          TagDecorate (stage 1)
                                            target: clothing.bottoms
                                            output: 3 bundles
                                                   │
ColorPalette(black, white, gray) ─► TagsExplode ───┤   (top color axis)
                                                   ▼
                                          TagDecorate (stage 2)
                                            target: clothing.uniform
                                            output: 3 × 3 = 9 bundles
                                                   │
                                                   ▼
                              CLIPTextEncode ─► KSampler ─► VAEDecode ─► PreviewImage
                                              (auto-fanout × 9)
```

Each `TagDecorate` has `INPUT_IS_LIST=True` and iterates
`bundle × decoration` internally, so stage 1 (1 base × 3 colors) emits
3 bundles, and stage 2 takes those 3 bundles × its own 3 colors → 9.
The preset's `pleated_skirt` becomes `<skirt_color> pleated skirt`;
its `serafuku` becomes `<top_color> serafuku`. ComfyUI's lazy fanout
runs `CLIPTextEncode` / `KSampler` / `VAEDecode` once per prompt, so
the preview lights up with all 9 variants without any extra wiring.

To extend further:

- **More variants on an existing axis**: check more boxes on the
  matching `ColorPalette`. The cross-product scales automatically.
- **More axes**: chain a third `TagDecorate` for, e.g.,
  `clothing.legwear` × thighhigh patterns. Each stage multiplies.
- **Different decoration types**: swap `ColorPalette` for
  `ClothingPattern` or `ClothingMaterial` on either axis.

The chained pattern is also covered as a regression in
`tests/integration/workflows.json` → `tag_decorate_chained_multiplies_axes`.
Same model-name caveat as `character_pipeline.json`.

### `inspector_debug.json`

Minimal debug-only graph (no model / sampler) for the **Tags: Bundle Inspector** node. Two tag-source nodes feed into `TagsMerge`, and the Inspector renders both the surviving bundle (grouped by layer/category) and the merge `warnings` in one OUTPUT_NODE preview.

```
BodyExposure(nude) ─────────┐
                            ├─► TagsMerge ─► (bundle)   ─► TagsBundleInspector
ClothingTops(shirt) ────────┘             └─► (warnings) ─►   (preview text)
```

Because `nude` triggers a TAG_CONFLICTS entry that drops all clothing, the Inspector preview shows `shirt` in the `--- dropped ---` section while `nude` survives under `[exposure]`. Drop the Inspector inline between `TagsMerge` and `CLIPTextEncode` in your own graphs to make conflict resolution visible at a glance.
