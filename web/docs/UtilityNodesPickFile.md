# Pick File

`UtilityNodes/Util` menu tree. A dropdown over any file in the input folder, no decoding — just a path (issue #28).

## Inputs

- `file`: a plain dropdown listing every file in the input folder, regardless of extension. There is no drag/drop upload button — ComfyUI's frontend only recognizes upload for a fixed set of content kinds (image/video/audio/mesh; see `Pick Image` / `Pick Video` / `Pick Audio` / `Pick Mesh`), with no generic "any file" kind to opt into. To get a new file into the dropdown, drop it into ComfyUI's `input/` folder directly, or upload it through one of the typed pickers first (they upload into the same folder).

## Outputs

- `path` (STRING): the resolved filesystem path of the picked file.

## Why

Some downstream nodes (generic file readers, files that aren't image/video/audio/mesh) just want a path to whatever's already sitting in the input folder, no upload UI needed for it.
