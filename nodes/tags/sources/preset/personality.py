from typing import Any, ClassVar

from ..._base import TAGS_TYPE, TaggedSelection

# Each personality preset is a bundle of expression / gaze / mouth / pose
# tags that together evoke an archetype. Designed to layer on top of
# CharacterPreset (or hand-built character bundles) via TagsMerge — the
# merge resolves any conflicting expressions through MUTEX_GROUPS.
PERSONALITY_PRESETS: dict[str, tuple[str, ...]] = {
    "tsundere": (
        "blush",
        "embarrassed",
        "pouting",
        "looking_away",
        "frown",
        "crossed_arms",
    ),
    "kuudere": (
        "expressionless",
        "narrowed_eyes",
        "closed_mouth",
        "serious",
        "looking_at_viewer",
    ),
    "yandere": (
        "yandere",
        "smirk",
        "narrowed_eyes",
        "heart-shaped_pupils",
        "looking_at_viewer",
    ),
    "dandere": (
        "shy",
        "light_blush",
        "looking_down",
        "embarrassed",
        "parted_lips",
        "hand_to_own_mouth",
    ),
    "genki": (
        "smile",
        "grin",
        "happy",
        "sparkling_eyes",
        "open_mouth",
        ":d",
        "blush_stickers",
    ),
    "ojou_sama": (
        "smug",
        "laughing",
        "hand_to_own_mouth",
        "looking_down",
        "hand_on_own_hip",
    ),
    "seiso": (
        "smile",
        "light_blush",
        "looking_at_viewer",
        "parted_lips",
    ),
    "gyaru": (
        "tan",
        "tanlines",
        "smirk",
        "smug",
        "sparkling_eyes",
        "looking_at_viewer",
    ),
    "mesugaki": (
        "smug_grin",
        "smug",
        "smirk",
        "narrowed_eyes",
        "looking_down",
        "hand_on_own_hip",
        "fang",
    ),
    "confident": (
        "smug",
        "grin",
        "looking_at_viewer",
        "hand_on_own_hip",
        "determined",
    ),
    "shy_girl": (
        "shy",
        "embarrassed",
        "blush",
        "looking_down",
        "hand_to_own_mouth",
    ),
    "sleepy": (
        "sleepy",
        "drowsy",
        "half-closed_eyes",
        "parted_lips",
        "messy_hair",
    ),
    "menhera": (
        "empty_eyes",
        "blank_eyes",
        "tearful",
        "sad",
        "bandages",
        "trembling",
    ),
    "apathetic": (
        "expressionless",
        "tired",
        "drowsy",
        "narrowed_eyes",
        "blank_expression",
    ),
    "airhead": (
        "blank_expression",
        "looking_up",
        "parted_lips",
        "ahoge",
        "light_blush",
    ),
    "hardboiled": (
        "serious",
        "narrowed_eyes",
        "looking_to_the_side",
        "smoking",
        "scar_on_cheek",
    ),
    "motherly": (
        "smile",
        "looking_down",
        "light_blush",
        "hand_on_another's_head",
    ),
    "playful_tease": (
        "smirk",
        "one_eye_closed",
        "tongue_out",
        "v",
    ),
    "scared": (
        "scared",
        "frightened",
        "wide-eyed",
        "trembling",
        "sweat",
    ),
    "angry_fierce": (
        "angry",
        "scowl",
        "glaring",
        "narrowed_eyes",
        "clenched_hands",
    ),
}


class PersonalityPreset:
    RETURN_TYPES: ClassVar[tuple[str, ...]] = (TAGS_TYPE,)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("bundle",)
    FUNCTION: ClassVar[str] = "build"
    CATEGORY: ClassVar[str] = "UtilityNodes/TagMaster/Preset"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "personality": (
                    sorted(PERSONALITY_PRESETS),
                    {"default": sorted(PERSONALITY_PRESETS)[0]},
                ),
            },
            "optional": {
                "extra": ("STRING", {"multiline": True, "default": ""}),
            },
        }

    def build(self, personality: str, extra: str = "") -> tuple[tuple[TaggedSelection, ...]]:
        tags = PERSONALITY_PRESETS.get(personality, ())
        bundle: list[TaggedSelection] = []
        if tags:
            bundle.append(
                TaggedSelection(
                    category=f"personality.{personality}",
                    layer="personality",
                    tags=tags,
                    mutex_within=False,
                )
            )
        extra_stripped = extra.strip()
        if extra_stripped:
            bundle.append(
                TaggedSelection(
                    category="extra",
                    layer="extra",
                    tags=(extra_stripped,),
                    mutex_within=False,
                )
            )
        return (tuple(bundle),)


NODE_CLASS_MAPPINGS: dict[str, type] = {"PersonalityPreset": PersonalityPreset}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"PersonalityPreset": "Personality"}
