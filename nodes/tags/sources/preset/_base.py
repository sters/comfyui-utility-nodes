from typing import Any, ClassVar

from ..._base import TAGS_TYPE, Spec, TaggedSelection

# Shared base for the flat-tuple preset nodes (character / personality /
# situation / nsfw_scene). Each subclass only declares its preset table,
# the input/parameter name, and the layer — everything else (INPUT_TYPES,
# build, SEARCH_ALIASES, the ComfyUI metadata) lives here.
#
# A preset is a flat tuple of tags. The merge node still applies
# TAG_CONFLICTS / MUTEX_GROUPS to the emitted bundle, so layering two
# presets, or layering a preset with regular tag-node selections, resolves
# cleanly downstream.

RANDOM_OPTION = "[random]"


class PresetNodeBase:
    # Subclasses override these three.
    PRESETS: ClassVar[dict[str, tuple[str, ...]]] = {}
    PARAM: ClassVar[str] = ""  # input socket / build kwarg name (e.g. "preset")
    LAYER: ClassVar[str] = ""  # layer + category prefix (e.g. "preset" -> "preset.<name>")

    RETURN_TYPES: ClassVar[tuple[str, ...]] = (TAGS_TYPE,)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("bundle",)
    FUNCTION: ClassVar[str] = "build"
    CATEGORY: ClassVar[str] = "UtilityNodes/TagMaster/Preset"
    SEARCH_ALIASES: ClassVar[list[str]] = []

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if "SEARCH_ALIASES" not in cls.__dict__:
            cls.SEARCH_ALIASES = sorted({*cls.PRESETS, *(t for v in cls.PRESETS.values() for t in v)})

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        names = [RANDOM_OPTION, *sorted(cls.PRESETS)]
        return {
            "required": {
                cls.PARAM: (names, {"default": RANDOM_OPTION}),
            },
            "optional": {
                "extra": ("STRING", {"multiline": True, "default": ""}),
            },
        }

    def _make_fixed(self, preset_name: str, tags: tuple[str, ...], extra_stripped: str) -> Spec:
        bundle: list[TaggedSelection] = []
        if tags:
            bundle.append(
                TaggedSelection(
                    category=f"{self.LAYER}.{preset_name}",
                    layer=self.LAYER,
                    tags=tags,
                    mutex_within=False,
                )
            )
        if extra_stripped:
            bundle.append(
                TaggedSelection(
                    category="extra",
                    layer="extra",
                    tags=(extra_stripped,),
                    mutex_within=False,
                )
            )
        return Spec(kind="fixed", pool=tuple(bundle))

    def build(self, *args: Any, extra: str = "", **kwargs: Any) -> tuple[Spec]:
        # ComfyUI calls build(<PARAM>=..., extra=...) by keyword; the tests
        # call build(<name>) positionally. Accept both.
        name = args[0] if args else kwargs.get(self.PARAM, "")
        extra_stripped = extra.strip()

        if name == RANDOM_OPTION:
            candidates = tuple(self._make_fixed(n, t, extra_stripped) for n, t in self.PRESETS.items())
            if not candidates:
                return (Spec(kind="fixed", pool=()),)
            return (Spec(kind="bundle_choice", bundles=candidates),)

        return (self._make_fixed(name, self.PRESETS.get(name, ()), extra_stripped),)
