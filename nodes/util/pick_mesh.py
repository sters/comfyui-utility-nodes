"""Choose a 3D mesh from the input folder, ComfyUI's native Load3D-style widget (issue #28)."""

from __future__ import annotations

from ._pick_base import PickNodeBase


class PickMesh(PickNodeBase):
    UPLOAD_KEY = "mesh_upload"
    CONTENT_TYPES = ("model",)


NODE_CLASS_MAPPINGS: dict[str, type] = {"UtilityNodesPickMesh": PickMesh}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"UtilityNodesPickMesh": "Pick Mesh"}
