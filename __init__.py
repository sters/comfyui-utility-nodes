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
    ("_cuun_random_text_picker", "nodes/random_text_picker.py"),
    ("_cuun_prompt_combinator", "nodes/prompt_combinator.py"),
    ("_cuun_list_shuffle", "nodes/list_shuffle.py"),
    ("_cuun_text_concat", "nodes/text_concat.py"),
    ("_cuun_pony_prompt_builder", "nodes/pony_prompt_builder.py"),
    ("_cuun_danbooru_bad_tags", "nodes/danbooru_bad_tags.py"),
    ("_cuun_composition_tags", "nodes/composition_tags.py"),
]:
    _mod = _load(_modname, _relpath)
    NODE_CLASS_MAPPINGS.update(_mod.NODE_CLASS_MAPPINGS)  # type: ignore[attr-defined]
    NODE_DISPLAY_NAME_MAPPINGS.update(_mod.NODE_DISPLAY_NAME_MAPPINGS)  # type: ignore[attr-defined]

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
