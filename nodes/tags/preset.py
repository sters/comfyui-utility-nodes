from typing import Any, ClassVar

from ._base import TAGS_TYPE, TaggedSelection

# Each preset is a flat tuple of tags. The merge node still applies
# TAG_CONFLICTS / MUTEX_GROUPS to the emitted bundle, so layering two
# presets, or layering a preset with regular tag-node selections, still
# resolves cleanly.
PRESETS: dict[str, tuple[str, ...]] = {
    "miko": (
        "long_hair",
        "black_hair",
        "bangs",
        "miko",
        "hakama",
        "tabi",
        "zouri",
        "shrine_outdoors",
    ),
    "serafuku_schoolgirl": (
        "long_hair",
        "black_hair",
        "bangs",
        "hair_ribbon",
        "serafuku",
        "sailor_collar",
        "pleated_skirt",
        "thighhighs",
        "loafers",
    ),
    "blazer_schoolgirl": (
        "medium_hair",
        "brown_hair",
        "blazer_uniform",
        "blouse",
        "pleated_skirt",
        "cardigan",
        "pantyhose",
        "loafers",
    ),
    "maid": (
        "long_hair",
        "twin_braids",
        "black_hair",
        "maid",
        "frilled_apron",
        "headband",
        "thighhighs",
        "mary_janes",
    ),
    "nurse": (
        "short_hair",
        "brown_hair",
        "medium_breasts",
        "nurse",
        "nurse_cap",
        "pantyhose",
        "loafers",
    ),
    "office_lady": (
        "medium_hair",
        "black_hair",
        "business_suit",
        "blouse",
        "pencil_skirt",
        "pantyhose",
        "high_heels",
        "glasses",
    ),
    "witch": (
        "very_long_hair",
        "purple_hair",
        "witch",
        "witch_hat",
        "long_dress",
        "thighhighs",
        "boots",
    ),
    "cheerleader": (
        "twintails",
        "orange_hair",
        "hair_ribbon",
        "cheerleader",
        "miniskirt",
        "socks",
        "sneakers",
    ),
    "yukata_festival": (
        "long_hair",
        "hair_bun",
        "ahoge",
        "hair_flower",
        "yukata",
        "obi",
        "tabi",
        "geta",
    ),
    "bunny_girl": (
        "long_hair",
        "ponytail",
        "black_hair",
        "bunny_girl",
        "bunny_ears",
        "rabbit_tail",
        "fishnets",
        "pantyhose",
        "high_heels",
    ),
    "princess": (
        "very_long_hair",
        "drill_hair",
        "blonde_hair",
        "pale_skin",
        "ball_gown",
        "tiara",
        "necklace",
        "elbow_gloves",
        "high_heels",
    ),
    "gothic_lolita": (
        "long_hair",
        "twin_drills",
        "black_hair",
        "pale_skin",
        "frilled_dress",
        "lace",
        "frills",
        "headband",
        "thighhighs",
        "mary_janes",
        "frilled_choker",
    ),
    "nun": (
        "long_hair",
        "silver_hair",
        "nun",
        "veil",
        "long_dress",
        "necklace",
    ),
    "kunoichi": (
        "long_hair",
        "ponytail",
        "black_hair",
        "toned",
        "kunoichi",
        "skin_tight",
        "tabi",
        "scarf_over_mouth",
    ),
    "catgirl_basic": (
        "long_hair",
        "cat_ears",
        "cat_tail",
        "yellow_eyes",
        "slit_pupils",
        "fang",
    ),
    "vampire": (
        "long_hair",
        "black_hair",
        "pale_skin",
        "pointy_ears",
        "fangs",
        "red_eyes",
        "cape",
        "long_dress",
    ),
    "santa_girl": (
        "long_hair",
        "twintails",
        "red_hair",
        "santa_costume",
        "santa_hat",
        "fur_trim",
        "thighhighs",
        "knee_boots",
    ),
    "knight": (
        "long_hair",
        "ponytail",
        "blonde_hair",
        "toned",
        "abs",
        "armor",
        "gauntlets",
        "pauldron",
        "vambraces",
        "cape",
        "knee_boots",
    ),
    "magical_girl": (
        "long_hair",
        "twintails",
        "pink_hair",
        "frilled_dress",
        "hair_ribbon",
        "tiara",
        "thighhighs",
        "mary_janes",
        "sparkles",
    ),
    "yandere_schoolgirl": (
        "very_long_hair",
        "black_hair",
        "red_eyes",
        "yandere",
        "smirk",
        "narrowed_eyes",
        "heart-shaped_pupils",
        "serafuku",
    ),
}


class CharacterPreset:
    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("STRING", TAGS_TYPE)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("prompt", "bundle")
    FUNCTION: ClassVar[str] = "build"
    CATEGORY: ClassVar[str] = "utility/text"
    OUTPUT_NODE: ClassVar[bool] = True

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "preset": (sorted(PRESETS), {"default": sorted(PRESETS)[0]}),
                "separator": ("STRING", {"multiline": False, "default": ", "}),
            },
            "optional": {
                "extra": ("STRING", {"multiline": True, "default": ""}),
            },
        }

    def build(self, preset: str, separator: str, extra: str = "") -> dict[str, Any]:
        sep = separator.encode("utf-8").decode("unicode_escape") if separator else ", "
        tags = PRESETS.get(preset, ())
        bundle: list[TaggedSelection] = []
        if tags:
            bundle.append(
                TaggedSelection(
                    category=f"preset.{preset}",
                    layer="preset",
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


NODE_CLASS_MAPPINGS: dict[str, type] = {"CharacterPreset": CharacterPreset}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"CharacterPreset": "Character Preset (full bundle)"}
