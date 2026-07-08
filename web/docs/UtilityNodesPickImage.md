# Pick Image

`UtilityNodes/Util` menu tree. A file chooser like the built-in **Load Image**, but emitting a path instead of a decoded tensor (issue #28).

## Inputs

- `file`: a dropdown over image files in the input folder, with the same drag/drop upload button and thumbnail preview `LoadImage` uses.

## Outputs

- `path` (STRING): the resolved filesystem path of the picked image.

## Why

Some downstream nodes (image-to-video pipelines, external tools invoked by path, …) just want a path, not a decoded `IMAGE` tensor. `Pick Image` gives you the same familiar upload/pick/preview UI as `LoadImage` without the decode step.

See also `Pick Video`, `Pick Audio`, `Pick Mesh` — ComfyUI's frontend only recognizes upload/preview for a fixed set of content kinds (image/video/audio/mesh), so each kind gets its own node rather than one generic "any file" picker.
