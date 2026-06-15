# Save Image with Metadata

`UtilityNodes/Image` category. Saves an `IMAGE` to the output folder exactly like the built-in **Save Image**, but embeds your own key/value pairs as PNG text chunks so they travel with the file. Read them back later with [Load Image with Metadata](UtilityNodesLoadImageWithMetadata.md) or [Extract Image Metadata](UtilityNodesExtractImageMetadata.md).

## Inputs

- `images` (IMAGE): the batch to save.
- `filename_prefix` (STRING, default `ComfyUI_meta`): output filename prefix (supports the usual `%date%` / subfolder tokens that Save Image accepts).
- `metadata` (STRING, multiline): the data to embed. Two formats are accepted:
  - **lines** — `key=value` or `key: value`, one per line. `=` wins over `:`, so values may contain colons (timestamps, URLs). Blank lines and `#` comments are ignored.
  - **JSON object** — e.g. `{"author": "sters", "seed": 42}`.
- `embed_workflow` (BOOLEAN, default `true`): also write the standard `prompt` / workflow chunks (keeps the image re-openable in ComfyUI). Turn it off to embed *only* your metadata.

## Outputs

- `filenames` (STRING): the saved file(s) as annotated paths (e.g. `ComfyUI_meta_00001_.png [output]`), one per line. Wire this straight into the `path` input of **Load Image with Metadata** / **Extract Image Metadata** to read the file back in the same graph.

This is also an output node — saved files appear in the node preview.

## Notes

- The standard chunks are skipped if ComfyUI was started with `--disable-metadata`, regardless of `embed_workflow`.
- Saves as PNG (lossless) so the text chunks survive.
