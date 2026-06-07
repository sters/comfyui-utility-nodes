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

Demonstrates `TagDecorate`'s **per-variant decoration** with the
Cartesian-product list semantics. A `CharacterPreset(serafuku_schoolgirl)`
bundle is decorated with three skirt colors at once → three prompts,
three KSampler runs, three images in the preview.

```
CharacterPreset(serafuku_schoolgirl) ─► TagsMerge ─┐
                                                   │
                                                   ▼
                                          TagDecorate ─► CLIPTextEncode ─► KSampler ─► VAEDecode ─► PreviewImage
                                            ▲   target: clothing.bottoms     (auto-fanout × 3)
                                            │
ColorPalette(red, green, blue) ─► TagsExplode ─► 3 single-color bundles (decoration axis)
```

`TagDecorate` has `INPUT_IS_LIST=True` so the 3 decoration bundles
become an axis: each `pleated_skirt` in the bundle is rewritten to
`<color> pleated skirt`, producing 3 prompts. ComfyUI's lazy fanout
propagates the list through `CLIPTextEncode` / `KSampler` / `VAEDecode`,
so you get 3 images per run with no extra wiring.

To add another axis (e.g. shirt color), **chain a second
`TagDecorate`** after this one with `target_category=clothing.tops`
and a different exploded decoration. Stage 1 emits 3 bundles, stage 2
multiplies to 3 × N — see the chained-decorate integration test
(`tag_decorate_chained_multiplies_axes` in `tests/integration/workflows.json`)
for the canonical wiring.

Same model-name caveat as `character_pipeline.json`.
