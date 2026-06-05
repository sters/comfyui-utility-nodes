import importlib.util
import sys
from pathlib import Path

_HERE = Path(__file__).parent


def _load(name: str, relpath: str) -> object:
    spec = importlib.util.spec_from_file_location(name, _HERE / relpath)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


NODE_CLASS_MAPPINGS: dict[str, type] = {}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {}

for _modname, _relpath in [
    ("_cuun_tag_node_base", "nodes/tags/_base.py"),
    ("_cuun_tags_conflicts", "nodes/tags/_conflicts.py"),
    ("_cuun_random_text_picker", "nodes/text/random_text_picker.py"),
    ("_cuun_prompt_combinator", "nodes/text/prompt_combinator.py"),
    ("_cuun_list_shuffle", "nodes/text/list_shuffle.py"),
    ("_cuun_text_concat", "nodes/text/text_concat.py"),
    ("_cuun_pony_prompt_builder", "nodes/text/pony_prompt_builder.py"),
    ("_cuun_bad_tags", "nodes/tags/bad.py"),
    ("_cuun_composition_tags", "nodes/tags/composition.py"),
    ("_cuun_hair_tags", "nodes/tags/body/hair.py"),
    ("_cuun_hands_tags", "nodes/tags/body/hands.py"),
    ("_cuun_feet_tags", "nodes/tags/body/feet.py"),
    ("_cuun_breasts_tags", "nodes/tags/body/breasts.py"),
    ("_cuun_body_type_tags", "nodes/tags/body/type.py"),
    ("_cuun_body_exposure_tags", "nodes/tags/body/exposure.py"),
    ("_cuun_body_marks_tags", "nodes/tags/body/marks.py"),
    ("_cuun_body_face_eyes", "nodes/tags/body/face/eyes.py"),
    ("_cuun_body_face_mouth", "nodes/tags/body/face/mouth.py"),
    ("_cuun_body_face_expression", "nodes/tags/body/face/expression.py"),
    ("_cuun_body_animal_features", "nodes/tags/body/animal_features.py"),
    ("_cuun_body_whole_pose", "nodes/tags/body/whole_pose.py"),
    ("_cuun_body_action", "nodes/tags/body/action.py"),
    ("_cuun_body_holding", "nodes/tags/body/holding.py"),
    ("_cuun_character_preset", "nodes/tags/preset.py"),
    ("_cuun_personality_preset", "nodes/tags/personality.py"),
    ("_cuun_meta_quality", "nodes/tags/meta/quality.py"),
    ("_cuun_meta_count", "nodes/tags/meta/count.py"),
    ("_cuun_scene_background", "nodes/tags/scene/background.py"),
    ("_cuun_scene_lighting", "nodes/tags/scene/lighting.py"),
    ("_cuun_scene_atmosphere", "nodes/tags/scene/atmosphere.py"),
    ("_cuun_clothing_state_tags", "nodes/tags/clothing/state.py"),
    ("_cuun_clothing_outfit_tags", "nodes/tags/clothing/outfit.py"),
    ("_cuun_clothing_underwear_swimwear_tags", "nodes/tags/clothing/underwear_swimwear.py"),
    ("_cuun_clothing_material_tags", "nodes/tags/clothing/material.py"),
    ("_cuun_clothing_legwear_footwear_tags", "nodes/tags/clothing/legwear_footwear.py"),
    ("_cuun_clothing_headwear_eyewear_tags", "nodes/tags/clothing/headwear_eyewear.py"),
    ("_cuun_clothing_accessory_tags", "nodes/tags/clothing/accessory.py"),
    ("_cuun_clothing_fit", "nodes/tags/clothing/fit.py"),
    ("_cuun_clothing_position", "nodes/tags/clothing/position.py"),
    ("_cuun_clothing_aside", "nodes/tags/clothing/aside.py"),
    ("_cuun_nsfw_act", "nodes/tags/nsfw/act.py"),
    ("_cuun_nsfw_position", "nodes/tags/nsfw/position.py"),
    ("_cuun_nsfw_state", "nodes/tags/nsfw/state.py"),
    ("_cuun_nsfw_solo_toy_bdsm", "nodes/tags/nsfw/solo_toy_bdsm.py"),
    ("_cuun_tags_merge", "nodes/tags/merge.py"),
]:
    _mod = _load(_modname, _relpath)
    NODE_CLASS_MAPPINGS.update(_mod.NODE_CLASS_MAPPINGS)  # type: ignore[attr-defined]
    NODE_DISPLAY_NAME_MAPPINGS.update(_mod.NODE_DISPLAY_NAME_MAPPINGS)  # type: ignore[attr-defined]

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
