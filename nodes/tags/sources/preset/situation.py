from typing import Any, ClassVar

from ..._base import TAGS_TYPE, TaggedSelection

# SFW situation/scene presets. Each bundle combines location + time-of-day +
# atmosphere + composition + action cues for a coherent scene. Designed to
# layer on top of CharacterPreset / PersonalityPreset via TagsMerge — the
# scene tags rarely conflict with character tags, so layering is usually
# clean. NSFW counterparts live in nsfw_preset.py.
#
# All tags here are constrained to be registered in some tag node (enforced
# by test_situation_preset.py) so that the prompt stays inside the index
# we already trust.
SITUATION_PRESETS: dict[str, tuple[str, ...]] = {
    "after_school_classroom": (
        "classroom",
        "indoors",
        "afternoon",
        "sunset",
        "backlighting",
        "school_uniform",
        "looking_at_viewer",
    ),
    "school_commute_morning": (
        "outdoors",
        "morning",
        "sunlight",
        "city",
        "cherry_blossoms",
        "school_uniform",
        "school_bag",
        "walking",
        "looking_at_viewer",
    ),
    "summer_beach": (
        "beach",
        "ocean",
        "outdoors",
        "noon",
        "sunny",
        "swimsuit",
        "wind_lift",
        "looking_at_viewer",
    ),
    "summer_festival": (
        "outdoors",
        "night",
        "festival",
        "yukata",
        "geta",
        "holding_hands",
        "looking_at_viewer",
        "happy",
        "smile",
    ),
    "winter_cafe": (
        "indoors",
        "cafe",
        "afternoon",
        "holding_cup",
        "sweater",
        "scarf",
        "smile",
        "looking_at_viewer",
    ),
    "hot_spring": (
        "steam",
        "night",
        "moonlight",
        "naked_towel",
        "blush",
        "looking_at_viewer",
    ),
    "shrine_visit": (
        "shrine",
        "outdoors",
        "afternoon",
        "miko",
        "hakama",
        "looking_at_viewer",
        "smile",
    ),
    "park_picnic": (
        "park",
        "outdoors",
        "noon",
        "sunny",
        "sitting",
        "smile",
        "looking_at_viewer",
    ),
    "library_study": (
        "library",
        "indoors",
        "afternoon",
        "holding_book",
        "school_uniform",
        "glasses",
        "from_side",
    ),
    "gym_workout": (
        "gym",
        "indoors",
        "gym_uniform",
        "sports_bra",
        "sweat",
        "panting",
        "looking_at_viewer",
        "dynamic_pose",
    ),
    "karaoke_room": (
        "indoors",
        "night",
        "neon_lights",
        "holding_microphone",
        "singing",
        "smile",
        "open_mouth",
    ),
    "shopping_date": (
        "outdoors",
        "city",
        "afternoon",
        "holding_hands",
        "happy",
        "smile",
        "looking_at_viewer",
    ),
    "morning_routine": (
        "bedroom",
        "indoors",
        "morning",
        "sunlight",
        "stretching",
        "messy_hair",
        "sleepy",
    ),
    "cherry_blossom_park": (
        "park",
        "outdoors",
        "cherry_blossoms",
        "petals",
        "noon",
        "sunlight",
        "school_uniform",
        "smile",
        "looking_at_viewer",
    ),
    "rooftop_sunset": (
        "rooftop",
        "outdoors",
        "evening",
        "sunset",
        "backlighting",
        "wind_lift",
        "school_uniform",
        "looking_at_viewer",
    ),
    "street_snap_city": (
        "outdoors",
        "city",
        "street",
        "afternoon",
        "walking",
        "from_below",
        "looking_at_viewer",
    ),
    "kitchen_cooking": (
        "kitchen",
        "indoors",
        "morning",
        "apron",
        "cooking",
        "smile",
        "looking_at_viewer",
    ),
    "snowy_streetscape": (
        "outdoors",
        "city",
        "snow",
        "evening",
        "scarf",
        "coat",
        "mittens",
        "smile",
        "looking_at_viewer",
    ),
}


class SituationPreset:
    RETURN_TYPES: ClassVar[tuple[str, ...]] = (TAGS_TYPE,)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("bundle",)
    FUNCTION: ClassVar[str] = "build"
    CATEGORY: ClassVar[str] = "UtilityNodes/TagMaster/Preset"
    OUTPUT_NODE: ClassVar[bool] = True

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "situation": (
                    sorted(SITUATION_PRESETS),
                    {"default": sorted(SITUATION_PRESETS)[0]},
                ),
                "separator": ("STRING", {"multiline": False, "default": ", "}),
            },
            "optional": {
                "extra": ("STRING", {"multiline": True, "default": ""}),
            },
        }

    def build(self, situation: str, separator: str, extra: str = "") -> dict[str, Any]:
        sep = separator.encode("utf-8").decode("unicode_escape") if separator else ", "
        tags = SITUATION_PRESETS.get(situation, ())
        bundle: list[TaggedSelection] = []
        if tags:
            bundle.append(
                TaggedSelection(
                    category=f"situation.{situation}",
                    layer="situation",
                    tags=tags,
                    mutex_within=False,
                )
            )
        parts = list(tags)
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


NODE_CLASS_MAPPINGS: dict[str, type] = {"SituationPreset": SituationPreset}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"SituationPreset": "Situation"}
