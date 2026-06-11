from typing import Any, ClassVar

# Max value ComfyUI uses for seed widgets (2**64 - 1).
_MAX_SEED = 0xFFFFFFFFFFFFFFFF


class SharedSeed:
    """A single shared seed value (issue #20).

    One `seed` INT widget with ComfyUI's *control after generate*
    (fixed / increment / decrement / randomize) wired out to multiple
    consumers — KSamplers, `TagsShuffle`, `TagsRandomPick`, etc. — so they
    all advance together instead of each carrying its own independent seed.

    Registered as `SharedSeed`, not the bare `Seed`: `Seed` is a class_type
    many popular packs (rgthree, Impact Pack, ...) also register, and
    ComfyUI's `NODE_CLASS_MAPPINGS` is a single global dict, so a duplicate
    key silently overwrites — whichever pack loads last wins and the rest
    vanish from the Add-Node menu (issue #25). The display name stays
    "Seed" so it's still what you search for.
    """

    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("INT",)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("seed",)
    FUNCTION: ClassVar[str] = "get"
    CATEGORY: ClassVar[str] = "UtilityNodes/Util"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "seed": (
                    "INT",
                    {"default": 0, "min": 0, "max": _MAX_SEED, "control_after_generate": True},
                ),
            },
        }

    def get(self, seed: int) -> tuple[int]:
        return (int(seed),)


NODE_CLASS_MAPPINGS: dict[str, type] = {"SharedSeed": SharedSeed}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"SharedSeed": "Seed"}
