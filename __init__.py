import importlib
import pkgutil

NODE_CLASS_MAPPINGS: dict[str, type] = {}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {}

# Auto-discover every module under nodes/ and merge its NODE_*_MAPPINGS.
# Skips files starting with `_` (e.g. _base.py, _conflicts.py).
#
# Guarded by __package__: when pytest accidentally collects this file as a
# bare module (no parent package), relative imports would explode. ComfyUI
# loads us as a real package, so the guard is a no-op there.
if __package__:
    from . import nodes

    for _finder, _name, _ispkg in pkgutil.walk_packages(nodes.__path__, nodes.__name__ + "."):
        if _ispkg or _name.rsplit(".", 1)[1].startswith("_"):
            continue
        _mod = importlib.import_module(_name)
        NODE_CLASS_MAPPINGS.update(getattr(_mod, "NODE_CLASS_MAPPINGS", {}))
        NODE_DISPLAY_NAME_MAPPINGS.update(getattr(_mod, "NODE_DISPLAY_NAME_MAPPINGS", {}))

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
