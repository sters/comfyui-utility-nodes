from dataclasses import dataclass
from typing import Any, ClassVar

NODE_CLASS_MAPPINGS: dict[str, type] = {}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {}

TAGS_TYPE = "CUUN_TAGS"

# tag string -> CATEGORY_ID of the TagNodeBase subclass that declares it.
# Populated by TagNodeBase.__init_subclass__ at import time. A tag declared by
# multiple subclasses sticks with the first registration (stable across runs
# because module import order is deterministic under pkgutil.walk_packages).
TAG_CATEGORY_REGISTRY: dict[str, str] = {}


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
    RETURN_TYPES: ClassVar[tuple[str, ...]] = (TAGS_TYPE,)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("bundle",)
    FUNCTION: ClassVar[str] = "build"
    CATEGORY: ClassVar[str] = "utility/text"
    OUTPUT_NODE: ClassVar[bool] = True

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if not cls.CATEGORY_ID:
            return
        for tag in cls.TAGS:
            TAG_CATEGORY_REGISTRY.setdefault(tag, cls.CATEGORY_ID)

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        required: dict[str, Any] = {
            "separator": ("STRING", {"multiline": False, "default": ", "}),
            "invert": ("BOOLEAN", {"default": False}),
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
        invert = bool(kwargs.pop("invert", False))
        tags: dict[str, bool] = {k: bool(v) for k, v in kwargs.items()}
        if invert:
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
        preview = sep.join(parts)
        return {"ui": {"text": (preview,)}, "result": (tuple(bundle),)}
