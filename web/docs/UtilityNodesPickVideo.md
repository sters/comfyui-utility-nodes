# Pick Video

`UtilityNodes/Util` menu tree. A file chooser like ComfyUI's built-in video loaders, but emitting a path instead of a decoded video (issue #28).

## Inputs

- `file`: a dropdown over video files in the input folder, with the same drag/drop upload button ComfyUI's built-in video-upload widget uses.

## Outputs

- `path` (STRING): the resolved filesystem path of the picked video.

## Why

Some downstream nodes (external tools invoked by path, custom decoders) just want a path, not a decoded video object. `Pick Video` gives you the same familiar upload/pick UI as ComfyUI's built-in video loaders without committing to a particular decoder.

See also `Pick Image`, `Pick Audio`, `Pick Mesh` — ComfyUI's frontend only recognizes upload/preview for a fixed set of content kinds (image/video/audio/mesh), so each kind gets its own node rather than one generic "any file" picker.
