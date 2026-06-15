# Load Image with Metadata

`UtilityNodes/Image` category. Loads an image from the input folder — same decode path as the built-in **Load Image** (EXIF transpose, RGB tensor, alpha → mask) — and additionally emits whatever metadata the file carries as a STRING.

## Inputs

- `image` (combo, upload): pick or upload a file from the input directory.

## Outputs

- `image` (IMAGE): the decoded RGB image.
- `mask` (MASK): the alpha channel inverted (zeros if the image has none).
- `metadata` (STRING): the file's embedded metadata, rendered as `key: value` lines — PNG text chunks (including any `prompt` / workflow JSON) plus decoded EXIF.

## Notes

- Pairs with [Save Image with Metadata](UtilityNodesSaveImageWithMetadata.md) for a full round-trip.
- For metadata only (no pixel decode, plus the format/size header), use [Extract Image Metadata](UtilityNodesExtractImageMetadata.md).
