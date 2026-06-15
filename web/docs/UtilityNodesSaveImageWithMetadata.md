# Save Image with Metadata

`UtilityNodes/Image` category. Saves an `IMAGE` to the output folder exactly like the built-in **Save Image**, but embeds your own key/value pairs as PNG text chunks so they travel with the file. Read them back later with [Load Image with Metadata](UtilityNodesLoadImageWithMetadata.md) or [Extract Image Metadata](UtilityNodesExtractImageMetadata.md).

## Inputs

- `images` (IMAGE): the batch to save.
- `filename_prefix` (STRING, default `ComfyUI_meta`): output filename prefix (supports the usual `%date%` / subfolder tokens that Save Image accepts).
- `metadata` (STRING, multiline): the data to embed. Two formats are accepted:
  - **lines** — `key=value` or `key: value`, one per line. `=` wins over `:`, so values may contain colons (timestamps, URLs). Blank lines and `#` comments are ignored.
  - **JSON object** — e.g. `{"author": "sters", "seed": 42}`.

## Outputs

None — this is an output node. Saved files appear in the node preview.

## Notes

- The standard `prompt` / workflow chunks are still written (so the image stays re-openable in ComfyUI), unless ComfyUI was started with `--disable-metadata`. Your custom keys are added on top.
- Saves as PNG (lossless) so the text chunks survive.
