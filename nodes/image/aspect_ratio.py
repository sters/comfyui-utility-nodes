from typing import Any, ClassVar

# Landscape (or square) only — `swap` flips to portrait at runtime so the
# preset list stays half the size and the user picks orientation
# separately from ratio. All dimensions are multiples of 64 so they
# round-trip cleanly through SDXL / Flux VAEs.
_PRESETS: dict[str, tuple[int, int]] = {
    "SDXL 1:1 (1024x1024)": (1024, 1024),
    "SDXL 5:4 (1152x896)": (1152, 896),
    "SDXL 3:2 (1216x832)": (1216, 832),
    "SDXL 16:9 (1344x768)": (1344, 768),
    "SDXL 21:9 (1536x640)": (1536, 640),
    "Hi-res 1:1 (1408x1408)": (1408, 1408),
    "Hi-res 3:2 (1536x1024)": (1536, 1024),
    "Hi-res 16:9 (1920x1088)": (1920, 1088),
}


class AspectRatioPreset:
    """Emit (width, height) INTs from a named SDXL / Flux-friendly preset.

    Five SDXL official bucket sizes (1MP-ish, landscape) plus three
    higher-resolution variants suited to Flux. `swap=True` flips to
    portrait. Wire `width` / `height` into `EmptyLatentImage` (or
    `EmptySD3LatentImage` etc.) to set the canvas dimensions.
    """

    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("INT", "INT")
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("width", "height")
    FUNCTION: ClassVar[str] = "resolve"
    CATEGORY: ClassVar[str] = "utility/image"
    OUTPUT_NODE: ClassVar[bool] = True

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "preset": (list(_PRESETS.keys()), {"default": next(iter(_PRESETS))}),
                "swap": ("BOOLEAN", {"default": False}),
            },
        }

    def resolve(self, preset: str, swap: bool) -> dict[str, Any]:
        w, h = _PRESETS.get(preset, (1024, 1024))
        if swap:
            w, h = h, w
        return {"ui": {"text": (f"{w}x{h}",)}, "result": (w, h)}


NODE_CLASS_MAPPINGS: dict[str, type] = {"AspectRatioPreset": AspectRatioPreset}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"AspectRatioPreset": "Aspect Ratio Preset"}
