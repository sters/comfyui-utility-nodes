"""Choose an image from the input folder, ComfyUI's native LoadImage-style widget (issue #28)."""

from __future__ import annotations

from ._pick_base import PickNodeBase


class PickImage(PickNodeBase):
    UPLOAD_KEY = "image_upload"
    CONTENT_TYPES = ("image",)


NODE_CLASS_MAPPINGS: dict[str, type] = {"UtilityNodesPickImage": PickImage}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"UtilityNodesPickImage": "Pick Image"}
