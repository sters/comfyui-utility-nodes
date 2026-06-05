from dataclasses import dataclass
from typing import Any, ClassVar

NODE_CLASS_MAPPINGS: dict[str, type] = {}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {}

TAGS_TYPE = "CUUN_TAGS"


@dataclass(frozen=True)
class TaggedSelection:
    """One categorized chunk of tags emitted by a tag-node.

    A node may emit multiple selections in a single bundle (e.g. its own
    tag list plus a free-form `extra` chunk).
    """

    category: str
    layer: str
    tags: tuple[str, ...]
    mutex_within: bool = False


class TagNodeBase:
    TAGS: ClassVar[tuple[str, ...]] = ()
    DEFAULT_BOOLEAN: ClassVar[bool] = False
    CATEGORY_ID: ClassVar[str] = ""
    LAYER: ClassVar[str] = ""
    MUTEX_WITHIN: ClassVar[bool] = False
    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("STRING", TAGS_TYPE)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("prompt", "bundle")
    FUNCTION: ClassVar[str] = "build"
    CATEGORY: ClassVar[str] = "utility/text"
    OUTPUT_NODE: ClassVar[bool] = True

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        required: dict[str, Any] = {
            "separator": ("STRING", {"multiline": False, "default": ", "}),
            "preset": (
                ["custom", "all_on", "all_off", "invert"],
                {"default": "custom"},
            ),
        }
        for tag in cls.TAGS:
            required[tag] = ("BOOLEAN", {"default": cls.DEFAULT_BOOLEAN})
        return {
            "required": required,
            "optional": {
                "extra": ("STRING", {"multiline": True, "default": ""}),
            },
        }

    def build(self, separator: str, extra: str = "", **kwargs: Any) -> dict[str, Any]:
        sep = separator.encode("utf-8").decode("unicode_escape") if separator else ", "
        preset = str(kwargs.pop("preset", "custom"))
        tags: dict[str, bool] = {k: bool(v) for k, v in kwargs.items()}
        if preset == "all_on":
            selected: list[str] = list(self.TAGS)
        elif preset == "all_off":
            selected = []
        elif preset == "invert":
            selected = [tag for tag in self.TAGS if not tags.get(tag, False)]
        else:
            selected = [tag for tag in self.TAGS if tags.get(tag, False)]

        bundle: list[TaggedSelection] = []
        if selected:
            bundle.append(
                TaggedSelection(
                    category=self.CATEGORY_ID,
                    layer=self.LAYER,
                    tags=tuple(selected),
                    mutex_within=self.MUTEX_WITHIN,
                )
            )
        parts = list(selected)
        extra_stripped = extra.strip()
        if extra_stripped:
            parts.append(extra_stripped)
            bundle.append(
                TaggedSelection(
                    category="extra",
                    layer="extra",
                    tags=(extra_stripped,),
                    mutex_within=False,
                )
            )
        prompt = sep.join(parts)
        return {"ui": {"text": (prompt,)}, "result": (prompt, tuple(bundle))}
