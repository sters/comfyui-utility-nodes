from typing import Any, ClassVar

from .._base import TAGS_TYPE, TaggedSelection

# NSFW scene presets — bundle act/position/state/expression/setting tags
# that frequently appear together. Designed to layer on top of
# CharacterPreset (visuals) and PersonalityPreset (mood) via TagsMerge.
# Conflicts with non-NSFW clothing presets are resolved automatically
# (e.g. `nude`-containing presets drop competing outfit tags).
NSFW_SCENE_PRESETS: dict[str, tuple[str, ...]] = {
    "vanilla_missionary": (
        "missionary",
        "vaginal",
        "kissing",
        "french_kiss",
        "nude",
        "blush",
        "parted_lips",
        "closed_eyes",
        "on_back",
    ),
    "doggystyle": (
        "doggystyle",
        "sex_from_behind",
        "arched_back",
        "all_fours",
        "ahegao",
        "heart-shaped_pupils",
        "tongue_out",
        "nude",
    ),
    "mating_press": (
        "mating_press",
        "ahegao",
        "heart-shaped_pupils",
        "on_back",
        "sweat",
        "blush",
        "nude",
        "tongue_out",
    ),
    "cowgirl_riding": (
        "cowgirl_position",
        "vaginal",
        "moaning",
        "blush",
        "looking_at_viewer",
        "open_mouth",
        "smirk",
        "nude",
    ),
    "anal_focus": (
        "anal",
        "anal_doggystyle",
        "cum_in_ass",
        "spread_ass",
        "presenting",
        "ahegao",
        "on_stomach",
    ),
    "fellatio_pov": (
        "fellatio",
        "cum_in_mouth",
        "saliva",
        "saliva_trail",
        "closed_eyes",
        "blush",
        "kneeling",
    ),
    "paizuri_scene": (
        "paizuri",
        "huge_breasts",
        "cum_on_breasts",
        "smirk",
        "looking_at_viewer",
        "topless",
    ),
    "handjob_dominant": (
        "handjob",
        "smirk",
        "looking_at_viewer",
        "looking_down",
        "smug",
    ),
    "footjob_dominant": (
        "footjob",
        "barefoot",
        "soles",
        "smug",
        "looking_down",
        "sitting",
    ),
    "after_sex_aftermath": (
        "after_sex",
        "cum_on_face",
        "cum_on_body",
        "ahegao",
        "drooling",
        "half-closed_eyes",
        "lying",
        "on_back",
        "sweat",
    ),
    "bukkake": (
        "bukkake",
        "cum_on_face",
        "cum_on_breasts",
        "cum_on_hair",
        "ahegao",
        "tongue_out",
        "open_mouth",
        "facial",
    ),
    "squirting": (
        "squirting",
        "female_ejaculation",
        "spread_legs",
        "ahegao",
        "on_back",
        "convulsing",
        "nude",
    ),
    "masturbation_solo": (
        "masturbation",
        "female_masturbation",
        "spread_pussy",
        "fingering",
        "blush",
        "heart-shaped_pupils",
        "parted_lips",
        "bedroom",
        "nude",
    ),
    "lingerie_tease": (
        "lingerie",
        "bra",
        "panties",
        "garter_belt",
        "thighhighs",
        "smirk",
        "looking_at_viewer",
        "bedroom",
        "on_back",
    ),
    "first_time_shy": (
        "vaginal",
        "missionary",
        "embarrassed",
        "blush",
        "tearful",
        "parted_lips",
        "nude",
        "closed_eyes",
    ),
    "femdom_dominant": (
        "smug",
        "looking_down",
        "bdsm",
        "leash",
        "thigh_boots",
        "corset",
        "spanking",
        "holding_whip",
    ),
    "bound_submissive": (
        "restrained",
        "tied_up",
        "ball_gag",
        "handcuffs",
        "blush",
        "embarrassed",
        "tearful",
        "nude",
    ),
    "shibari_suspension": (
        "shibari",
        "rope",
        "suspension_bondage",
        "bdsm",
        "ahegao",
        "nude",
        "blush",
    ),
    "breast_play": (
        "nipple_sucking",
        "breast_sucking",
        "breast_grab",
        "areola_slip",
        "nipples",
        "blush",
        "topless",
    ),
    "public_exposure": (
        "bottomless",
        "no_panties",
        "embarrassed",
        "blush",
        "bare_legs",
        "park",
        "outdoors",
        "looking_away",
    ),
    "shower_scene": (
        "bathroom",
        "shower",
        "steam",
        "wet_clothes",
        "blush",
        "embarrassed",
        "nude",
        "shiny_skin",
    ),
    "threesome_ffm": (
        "threesome",
        "ffm_threesome",
        "multiple_girls",
        "sweat",
        "blush",
    ),
    "panty_shot_voyeur": (
        "skirt_lift",
        "wind_lift",
        "panties",
        "exposed_gusset",
        "pleated_skirt",
        "blush",
        "looking_back",
        "embarrassed",
    ),
}


class NsfwScenePreset:
    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("STRING", TAGS_TYPE)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("prompt", "bundle")
    FUNCTION: ClassVar[str] = "build"
    CATEGORY: ClassVar[str] = "utility/text"
    OUTPUT_NODE: ClassVar[bool] = True

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "scene": (
                    sorted(NSFW_SCENE_PRESETS),
                    {"default": sorted(NSFW_SCENE_PRESETS)[0]},
                ),
                "separator": ("STRING", {"multiline": False, "default": ", "}),
            },
            "optional": {
                "extra": ("STRING", {"multiline": True, "default": ""}),
            },
        }

    def build(self, scene: str, separator: str, extra: str = "") -> dict[str, Any]:
        sep = separator.encode("utf-8").decode("unicode_escape") if separator else ", "
        tags = NSFW_SCENE_PRESETS.get(scene, ())
        bundle: list[TaggedSelection] = []
        if tags:
            bundle.append(
                TaggedSelection(
                    category=f"nsfw_preset.{scene}",
                    layer="nsfw_preset",
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
        prompt = sep.join(parts)
        return {"ui": {"text": (prompt,)}, "result": (prompt, tuple(bundle))}


NODE_CLASS_MAPPINGS: dict[str, type] = {"NsfwScenePreset": NsfwScenePreset}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"NsfwScenePreset": "NSFW Scene Preset (act / position / state)"}
