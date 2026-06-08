# Workflow templates

JSON files in this directory are picked up by ComfyUI's [Workflow
Templates](https://docs.comfy.org/custom-nodes/workflow_templates)
feature and surfaced under **Workflow → Browse Templates → comfyui-utility-nodes**.

## Templates

### `pony_sdxl_pipeline.json`

Pony Diffusion V6 XL (SDXL) text-to-image graph at the model's native
**1024×1024**. Shows the recommended Pony layout where `MetaPony` supplies
the `score_* / rating_* / source_*` prefix and the `extra` field carries
free-form text into both the positive and negative streams:

```
MetaPony(scores+rating_safe+source_anime, extra="1girl, solo") ─┐
CharacterPreset(witch) ─┤
PersonalityPreset(confident) ─┼─► TagsMerge ─► CLIPTextEncode (positive)
SituationPreset(summer_beach) ─┤
MetaQuality(masterpiece, best_quality, very_aesthetic) ─┘        │
                                                                 │
MetaPony(scores off, extra="worst quality, low quality, …") ─┐   │
BadGeneral ──────────────────────────────────────────────────┼─► TagsMerge ─► CLIPTextEncode (negative)
                                                                 │
CheckpointLoader(autismmixSDXL_autismmixPony) ─┬─► MODEL ────────►│ KSampler ─► VAEDecode ─► PreviewImage
                                               ├─► CLIP           │  (euler_ancestral, 25 steps, cfg 7)
                                               └─► VAE ──────────►│
EmptyLatentImage(1024×1024×1) ──────────────────────────────────►│
```

The negative `MetaPony` keeps every score off and uses `extra` for the
quality-negative phrase — a clean way to author the Pony negative without a
dedicated text node. Replace the checkpoint name with your local Pony
checkpoint. The positive/negative text portions are mirrored as
`pony_sdxl_pipeline_positive` / `_negative` in
`tests/integration/workflows.json`.

### `character_pipeline.json`

End-to-end text-to-image graph that demonstrates the recommended
positive-prompt pipeline:

```
CharacterPreset(miko) ─┐
PersonalityPreset(genki) ─┤
SituationPreset(shrine_visit) ─┼─► TagsMerge ─► CLIPTextEncode (positive)
MetaQuality ─┘                                           │
                                                         │
BadGeneral ─► TagsMerge ─► CLIPTextEncode (negative) ────│
                                                         │
CheckpointLoader ─┬─► MODEL ────────────────────────────►│ KSampler ─► VAEDecode ─► PreviewImage
                  ├─► CLIP (both encoders)               │
                  └─► VAE ──────────────────────────────►│
EmptyLatentImage(512×512×1) ────────────────────────────►│
```

> Every tag node now emits only a `bundle` (CUUN_TAGS) — to turn a bundle into
> the STRING a `CLIPTextEncode` needs, route it through `TagsMerge`. That's why
> the negative side gains a small `BadGeneral ─► TagsMerge` hop.

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
                  TagsMerge ─► CLIPTextEncode ─► KSampler ─► VAEDecode ─► PreviewImage
                  (bundle→STRING) (auto-fanout × 9)
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
