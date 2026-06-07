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
