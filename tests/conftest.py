import importlib.util
import sys
from pathlib import Path

_NODES = Path(__file__).parent.parent / "nodes" / "tags"

for _name, _path in [
    ("_cuun_tag_node_base", _NODES / "_base.py"),
    ("_cuun_tags_conflicts", _NODES / "_conflicts.py"),
]:
    if _name in sys.modules:
        continue
    _spec = importlib.util.spec_from_file_location(_name, _path)
    assert _spec and _spec.loader
    _mod = importlib.util.module_from_spec(_spec)
    sys.modules[_name] = _mod
    _spec.loader.exec_module(_mod)
