# Load Image with Metadata

`UtilityNodes/Image` category. Loads an image — same decode path as the built-in **Load Image** (EXIF transpose, RGB tensor, alpha → mask) — and additionally emits whatever metadata the file carries as a STRING.

## Inputs

- `image` (combo, upload): pick or upload a file from the input directory.
- `path` (STRING, optional): an annotated filepath such as `foo.png [output]`. When set it **overrides** `image`, so a file just written by [Save Image with Metadata](UtilityNodesSaveImageWithMetadata.md) (whose `filenames` output is exactly this form) can be loaded back in the same graph.

## Outputs

- `image` (IMAGE): the decoded RGB image.
- `mask` (MASK): the alpha channel inverted (zeros if the image has none).
- `metadata` (STRING): the file's embedded metadata, rendered as `key: value` lines — PNG text chunks (including any `prompt` / workflow JSON) plus decoded EXIF.

## Notes

- Pairs with [Save Image with Metadata](UtilityNodesSaveImageWithMetadata.md) for a full round-trip.
- For metadata only (no pixel decode, plus the format/size header), use [Extract Image Metadata](UtilityNodesExtractImageMetadata.md).
