"""Choose any file from the input folder — the fallback for types the typed pickers don't cover (issue #28)."""

from __future__ import annotations

from ._pick_base import PickNodeBase


class PickFile(PickNodeBase):
    """UPLOAD_KEY/CONTENT_TYPES stay unset: a plain dropdown over every file, no upload button."""


NODE_CLASS_MAPPINGS: dict[str, type] = {"UtilityNodesPickFile": PickFile}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"UtilityNodesPickFile": "Pick File"}
