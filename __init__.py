import importlib
import logging
import pkgutil

NODE_CLASS_MAPPINGS: dict[str, type] = {}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {}

# Every registered class_type is namespaced with this prefix so it can never be
# shadowed by another pack's same-named node (ComfyUI keeps all custom nodes in
# one global NODE_CLASS_MAPPINGS dict — duplicate keys silently overwrite, and
# the loser vanishes from the menu; see issue #25). The Python class names and
# the human-facing display names stay unprefixed.
_KEY_PREFIX = "UtilityNodes"

# Renames of an *already-prefixed* class_type (as opposed to the bare->prefixed
# migration below, which is derived automatically) need an explicit entry here
# so already-saved workflows still auto-upgrade instead of showing "undefined
# node". Add one line per such rename; never remove an old entry once shipped.
_LEGACY_RENAMES = {
    "UtilityNodesTagsMerge": "UtilityNodesTagsBuild",
    "UtilityNodesNsfwScenePreset": "UtilityNodesNsfwActPreset",
}


def _register_node_replacements() -> None:
    """Tell ComfyUI that old class_types were renamed, so already-saved
    workflows auto-upgrade on load instead of showing "undefined node".

    Two sources of renames, both pure (only the class_type string changed;
    inputs/outputs are identical), so each replacement is just old_id ->
    new_id:

    1. Bare -> prefixed (derived automatically from every current
       `NODE_CLASS_MAPPINGS` key — see `_KEY_PREFIX`).
    2. Prefixed -> prefixed (explicit, see `_LEGACY_RENAMES`).

    The loader treats V1 NODE_CLASS_MAPPINGS and the V3 `comfy_entrypoint` as
    mutually exclusive (`if ... elif ...`), so we can't register via a
    ComfyExtension while keeping our V1 mappings — instead we call the
    (synchronous) NodeReplaceManager directly, exactly as
    `ComfyAPI().node_replacement.register` does internally.

    Guarded end-to-end: on a ComfyUI too old to have the manager (or before the
    server instance exists), this is a silent no-op and the nodes still load.
    `apply_replacements` only fires when the old id is absent from
    NODE_CLASS_MAPPINGS, so this never hijacks another pack's same-named node.
    """
    try:
        from comfy_api.latest import io
        from server import PromptServer

        manager = PromptServer.instance.node_replace_manager
    except Exception:  # ComfyUI lacks the API, or the server isn't up yet.
        return

    _renames = dict(_LEGACY_RENAMES)
    for _new_id in NODE_CLASS_MAPPINGS:
        if _new_id.startswith(_KEY_PREFIX):
            _renames[_new_id[len(_KEY_PREFIX) :]] = _new_id

    for _old_id, _new_id in _renames.items():
        try:
            manager.register(io.NodeReplace(old_node_id=_old_id, new_node_id=_new_id))
        except Exception as _e:  # never let one bad mapping break node loading
            logging.warning("comfyui-utility-nodes: failed to register replacement %s -> %s: %s", _old_id, _new_id, _e)


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

    _register_node_replacements()

WEB_DIRECTORY = "./web"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
