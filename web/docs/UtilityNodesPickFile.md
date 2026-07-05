# Pick File

`UtilityNodes/Util` menu tree. A file chooser like the built-in **Load Image**, but for any file — no decoding, just a path (issue #28).

## Inputs

- `file`: a dropdown over the input folder, with a drag/drop upload button (same widget `LoadImage` uses). If the picked file looks like an image (by extension), a thumbnail preview is shown on the node, same as `LoadImage`; for any other file type, no preview is attempted.

## Outputs

- `path` (STRING): the resolved filesystem path of the picked file.

## Why

Some downstream nodes (video loaders, audio loaders, generic file readers) just want a path, not a decoded tensor. `Pick File` gives you the same familiar upload/pick UI as `LoadImage` without committing to any particular file type.
