# Aspect Ratio Preset

`UtilityNodes/Image` category. Emits `(width, height)` INTs from a named SDXL / Flux-friendly resolution preset. Saves the round-trip through "what was the 16:9 bucket size again?" — feed the outputs into `EmptyLatentImage` (or `EmptySD3LatentImage` etc.) to set the canvas.

## Inputs

- `preset` (combo): a named resolution. All presets are stored as **landscape (or square)**.
  - `SDXL 1:1 (1024x1024)`
  - `SDXL 5:4 (1152x896)`
  - `SDXL 3:2 (1216x832)`
  - `SDXL 16:9 (1344x768)`
  - `SDXL 21:9 (1536x640)`
  - `Hi-res 1:1 (1408x1408)`
  - `Hi-res 3:2 (1536x1024)`
  - `Hi-res 16:9 (1920x1088)`
- `swap` (BOOLEAN, default `false`): flip width and height to get portrait orientation.

## Outputs

- `width` (INT), `height` (INT).

## Notes

- All dimensions are multiples of 64 — safe for SDXL / Flux VAE strides.
- The five `SDXL` entries are the official ~1MP training buckets. The three `Hi-res` entries are higher-resolution variants that Flux handles comfortably (and SDXL can use with refinement / tiled VAE).
- The node previews the resolved `WxH` string in the UI so you can verify swap / preset at a glance.
