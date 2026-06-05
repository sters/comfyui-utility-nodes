import importlib.util
import sys
from pathlib import Path

_BASE = Path(__file__).parent.parent / "nodes" / "tags" / "_base.py"
if "_cuun_tag_node_base" not in sys.modules:
    _spec = importlib.util.spec_from_file_location("_cuun_tag_node_base", _BASE)
    assert _spec and _spec.loader
    _mod = importlib.util.module_from_spec(_spec)
    sys.modules["_cuun_tag_node_base"] = _mod
    _spec.loader.exec_module(_mod)
