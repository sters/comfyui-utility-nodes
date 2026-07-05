"""File picker node (issue #28).

``PickFile`` mirrors the built-in ``LoadImage`` chooser widget — a dropdown
over the input folder plus a drag/drop upload button — but never decodes
anything. It just resolves the pick to a real filesystem path, so any file
(not only images) can be wired downstream as a plain STRING path.

``web/js/pick_file_preview.js`` adds the same thumbnail preview ``LoadImage``
shows, but only when the picked filename looks like an image (by extension) —
unlike ``LoadImage``'s built-in ``image_upload`` widget config, which always
assumes the pick is an image, this node's picks can be anything.

``folder_paths`` is a ComfyUI-runtime module, so it is imported lazily inside
the methods — the module stays importable without it installed. There is no
pure logic to unit-test here (the whole body is folder_paths delegation), so
unlike the parse/format helpers in ``nodes/image/metadata.py`` this node has
no accompanying test file — consistent with the other loader nodes in this
repo (e.g. ``LoadImageWithMetadata.load``).
"""

from __future__ import annotations

from typing import Any, ClassVar


class PickFile:
    """Choose a file from the input folder (or upload one) and emit its resolved path."""

    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("STRING",)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("path",)
    FUNCTION: ClassVar[str] = "pick"
    CATEGORY: ClassVar[str] = "UtilityNodes/Util"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        import os

        import folder_paths

        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        return {
            "required": {
                "file": (sorted(files), {"file_upload": True}),
            },
        }

    def pick(self, file: str) -> tuple[str]:
        import folder_paths

        return (folder_paths.get_annotated_filepath(file),)

    @classmethod
    def IS_CHANGED(cls, file: str) -> str:
        import folder_paths

        return folder_paths.get_annotated_filepath(file)  # type: ignore[no-any-return]

    @classmethod
    def VALIDATE_INPUTS(cls, file: str) -> bool | str:
        import folder_paths

        if not folder_paths.exists_annotated_filepath(file):
            return f"Invalid file: {file}"
        return True


NODE_CLASS_MAPPINGS: dict[str, type] = {"UtilityNodesPickFile": PickFile}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"UtilityNodesPickFile": "Pick File"}
