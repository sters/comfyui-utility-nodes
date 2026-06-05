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
    ("_cuun_clothing_state_tags", "nodes/tags/clothing/state.py"),
    ("_cuun_clothing_outfit_tags", "nodes/tags/clothing/outfit.py"),
    ("_cuun_clothing_underwear_swimwear_tags", "nodes/tags/clothing/underwear_swimwear.py"),
    ("_cuun_clothing_material_tags", "nodes/tags/clothing/material.py"),
    ("_cuun_clothing_legwear_footwear_tags", "nodes/tags/clothing/legwear_footwear.py"),
    ("_cuun_clothing_headwear_eyewear_tags", "nodes/tags/clothing/headwear_eyewear.py"),
    ("_cuun_clothing_accessory_tags", "nodes/tags/clothing/accessory.py"),
    ("_cuun_nsfw_act", "nodes/tags/nsfw/act.py"),
    ("_cuun_nsfw_position", "nodes/tags/nsfw/position.py"),
    ("_cuun_nsfw_state", "nodes/tags/nsfw/state.py"),
    ("_cuun_nsfw_solo_toy_bdsm", "nodes/tags/nsfw/solo_toy_bdsm.py"),
]:
    _mod = _load(_modname, _relpath)
    NODE_CLASS_MAPPINGS.update(_mod.NODE_CLASS_MAPPINGS)  # type: ignore[attr-defined]
    NODE_DISPLAY_NAME_MAPPINGS.update(_mod.NODE_DISPLAY_NAME_MAPPINGS)  # type: ignore[attr-defined]

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
