"""Choose an audio file from the input folder, ComfyUI's native LoadAudio-style widget (issue #28)."""

from __future__ import annotations

from ._pick_base import PickNodeBase


class PickAudio(PickNodeBase):
    UPLOAD_KEY = "audio_upload"
    CONTENT_TYPES = ("audio",)


NODE_CLASS_MAPPINGS: dict[str, type] = {"UtilityNodesPickAudio": PickAudio}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"UtilityNodesPickAudio": "Pick Audio"}
