from typing import Any, ClassVar

# Max value ComfyUI uses for seed widgets (2**64 - 1).
_MAX_SEED = 0xFFFFFFFFFFFFFFFF


class Seed:
    """A single shared seed value (issue #20).

    One `seed` INT widget with ComfyUI's *control after generate*
    (fixed / increment / decrement / randomize) wired out to multiple
    consumers — KSamplers, `TagsShuffle`, `TagsRandomPick`, etc. — so they
    all advance together instead of each carrying its own independent seed.
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


NODE_CLASS_MAPPINGS: dict[str, type] = {"Seed": Seed}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"Seed": "Seed"}
