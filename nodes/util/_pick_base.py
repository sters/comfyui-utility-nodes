"""Shared body for the ``Pick*`` file-picker nodes (issue #28).

ComfyUI's frontend hardcodes upload+preview behavior to a fixed set of combo
widget config keys — ``image_upload``, ``video_upload``, ``audio_upload``,
``mesh_upload`` (and ``animated_image_upload``) — with no generic "any file"
kind, so a single file-type-agnostic picker can't get native upload/preview
for free (confirmed by decompiling the shipped frontend bundle: the widget
selector reads exactly those keys off the combo's options dict and nothing
else). So there's one node per kind ComfyUI natively recognizes, each using
the matching ``folder_paths.filter_files_content_types`` filter so the
dropdown only lists files of that kind, exactly like the built-in loaders
(``LoadImage`` filters to ``["image"]``, ``LoadAudio`` to ``["audio"]``, …).

``PickFile`` is the odd one out: it leaves ``UPLOAD_KEY``/``CONTENT_TYPES``
unset, so the base class skips both the upload-kind config key and the
content-type filter — a plain dropdown over every file in the input folder,
any extension, with no upload button (there being no generic upload kind to
opt into). It's the fallback for file types the four typed pickers don't
cover.

``folder_paths`` is a ComfyUI-runtime module, so it is imported lazily inside
the methods — the module stays importable without it installed. There is no
pure logic to unit-test here (the whole body is folder_paths delegation), so
unlike the parse/format helpers in ``nodes/image/metadata.py`` these nodes
have no accompanying test file — consistent with the other loader nodes in
this repo (e.g. ``LoadImageWithMetadata.load``).
"""

from __future__ import annotations

from typing import Any, ClassVar, Literal


class PickNodeBase:
    """Choose a file of one content type from the input folder (or upload one) and emit its resolved path."""

    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("STRING",)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("path",)
    FUNCTION: ClassVar[str] = "pick"
    CATEGORY: ClassVar[str] = "UtilityNodes/Util"

    # Subclasses set these: UPLOAD_KEY is the combo config key ComfyUI's frontend
    # recognizes for this kind (e.g. "image_upload"); CONTENT_TYPES filters the
    # dropdown via folder_paths.filter_files_content_types. Left unset (None),
    # the dropdown lists every file with no upload button — PickFile's case.
    UPLOAD_KEY: ClassVar[str | None] = None
    CONTENT_TYPES: ClassVar[tuple[Literal["image", "video", "audio", "model"], ...] | None] = None

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        import os

        import folder_paths

        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        if cls.CONTENT_TYPES is not None:
            files = folder_paths.filter_files_content_types(files, list(cls.CONTENT_TYPES))
        options: dict[str, bool] = {cls.UPLOAD_KEY: True} if cls.UPLOAD_KEY is not None else {}
        return {
            "required": {
                "file": (sorted(files), options),
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
