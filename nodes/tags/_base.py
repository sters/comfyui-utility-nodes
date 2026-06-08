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

# Hierarchical category root for ComfyUI's Add Node menu. Subpackages under
# `nodes/` mirror into nested entries beneath this root (see `category_for_module`).
ROOT_CATEGORY = "UtilityNodes"

# Segment-name overrides for parts that don't title-case cleanly.
_SEGMENT_OVERRIDES = {
    "tags": "TagMaster",
    "nsfw": "NSFW",
    "tagmaster": "TagMaster",
}


def category_for_module(module: str) -> str:
    """Map a node module's dotted path to its ComfyUI category.

    `nodes.tags.sources.body.hair` → `UtilityNodes/TagMaster/Body`
    `nodes.tags.sources.body.face.eyes` → `UtilityNodes/TagMaster/Body/Face`
    `nodes.tags.merge` → `UtilityNodes/TagMaster`
    `nodes.image.aspect_ratio` → `UtilityNodes/Image`

    ComfyUI imports this pack under its directory name as the top-level
    package, so a node's `__module__` is prefixed (e.g.
    `comfyui-utility-nodes.nodes.tags.sources.body.hair`), whereas the test
    suite imports modules as bare `nodes.tags...`. Anchor on the `nodes`
    package segment wherever it appears so both resolve identically — without
    this, every node on ComfyUI fell back to the bare `UtilityNodes` root.
    """
    parts = module.split(".")
    if "nodes" not in parts:
        return ROOT_CATEGORY
    # Drop everything up to and including the `nodes` package segment, plus the
    # trailing filename segment.
    parts = parts[parts.index("nodes") + 1 : -1]
    # Collapse `tags.sources` → `tags` so the menu reads "TagMaster/Body" not
    # "TagMaster/Sources/Body".
    if len(parts) >= 2 and parts[0] == "tags" and parts[1] == "sources":
        parts = ["tags", *parts[2:]]
    out: list[str] = [ROOT_CATEGORY]
    for p in parts:
        out.append(_SEGMENT_OVERRIDES.get(p.lower(), p.title()))
    return "/".join(out)


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
    CATEGORY: ClassVar[str] = ROOT_CATEGORY
    OUTPUT_NODE: ClassVar[bool] = True

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        # Subclasses inherit the bare root category by default; override it
        # with the module-derived hierarchical category unless the subclass
        # spelled out its own CATEGORY.
        if cls.CATEGORY == TagNodeBase.CATEGORY:
            cls.CATEGORY = category_for_module(cls.__module__)
        if not cls.CATEGORY_ID:
            return
        for tag in cls.TAGS:
            TAG_CATEGORY_REGISTRY.setdefault(tag, cls.CATEGORY_ID)

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        required: dict[str, Any] = {
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

    def build(self, extra: str = "", **kwargs: Any) -> dict[str, Any]:
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
        preview = ", ".join(parts)
        return {"ui": {"text": (preview,)}, "result": (tuple(bundle),)}
