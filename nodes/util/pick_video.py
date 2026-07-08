"""Choose a video from the input folder, ComfyUI's native video-upload widget (issue #28)."""

from __future__ import annotations

from ._pick_base import PickNodeBase


class PickVideo(PickNodeBase):
    UPLOAD_KEY = "video_upload"
    CONTENT_TYPES = ("video",)


NODE_CLASS_MAPPINGS: dict[str, type] = {"UtilityNodesPickVideo": PickVideo}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"UtilityNodesPickVideo": "Pick Video"}
