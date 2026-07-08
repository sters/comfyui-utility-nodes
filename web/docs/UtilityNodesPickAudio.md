# Pick Audio

`UtilityNodes/Util` menu tree. A file chooser like the built-in **Load Audio**, but emitting a path instead of a decoded waveform (issue #28).

## Inputs

- `file`: a dropdown over audio files in the input folder, with the same drag/drop upload button `LoadAudio` uses.

## Outputs

- `path` (STRING): the resolved filesystem path of the picked audio file.

## Why

Some downstream nodes (external tools invoked by path, custom decoders) just want a path, not a decoded `AUDIO` value. `Pick Audio` gives you the same familiar upload/pick UI as `LoadAudio` without the decode step.

See also `Pick Image`, `Pick Video`, `Pick Mesh` — ComfyUI's frontend only recognizes upload/preview for a fixed set of content kinds (image/video/audio/mesh), so each kind gets its own node rather than one generic "any file" picker.
