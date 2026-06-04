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


_random_text_picker = _load("_cuun_random_text_picker", "nodes/random_text_picker.py")

NODE_CLASS_MAPPINGS = _random_text_picker.NODE_CLASS_MAPPINGS  # type: ignore[attr-defined]
NODE_DISPLAY_NAME_MAPPINGS = _random_text_picker.NODE_DISPLAY_NAME_MAPPINGS  # type: ignore[attr-defined]

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
