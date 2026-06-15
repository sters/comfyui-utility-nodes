# Extract Image Metadata

`UtilityNodes/Image` category. Reads *every* piece of metadata from a media file in the input folder and emits it as a STRING. Unlike [Load Image with Metadata](UtilityNodesLoadImageWithMetadata.md), it never decodes the pixels into a tensor — it just opens the header — so it's handy for inspecting what a generator wrote, or recovering a prompt from a saved PNG.

## Inputs

- `image` (combo, upload): pick or upload a file from the input directory.

## Outputs

- `metadata` (STRING): `key: value` lines covering:
  - a `format` / `size` / `mode` header (e.g. `PNG`, `1024x1024`, `RGBA`),
  - PNG text chunks (including any `prompt` / workflow JSON),
  - decoded EXIF tags (mapped to human-readable names where known).

## Notes

- Works on any format PIL can open (PNG, JPEG, WebP, …). EXIF is most common on JPEG; text chunks on PNG.
- Wire the output into a `PreviewAny` (or any STRING-consuming node) to read it on the canvas.
