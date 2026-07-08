# Pick Mesh

`UtilityNodes/Util` menu tree. A file chooser like ComfyUI's built-in **Load 3D**, but emitting a path instead of a decoded mesh (issue #28).

## Inputs

- `file`: a dropdown over 3D model files in the input folder, with the same drag/drop upload button ComfyUI's built-in mesh-upload widget uses.

## Outputs

- `path` (STRING): the resolved filesystem path of the picked mesh.

## Why

Some downstream nodes (external tools invoked by path, custom loaders) just want a path, not a decoded mesh object. `Pick Mesh` gives you the same familiar upload/pick UI as ComfyUI's built-in 3D loaders without committing to a particular loader.

See also `Pick Image`, `Pick Video`, `Pick Audio` — ComfyUI's frontend only recognizes upload/preview for a fixed set of content kinds (image/video/audio/mesh), so each kind gets its own node rather than one generic "any file" picker.
