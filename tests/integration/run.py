"""Integration check against a running ComfyUI instance.

Reads `workflows.json`, posts each workflow to ComfyUI's `/prompt`
endpoint, polls `/history/<prompt_id>` until completion, and asserts
that each expected string equals (exactly) one of the text outputs of
the named node.

The pack's own nodes are pure data nodes (no OUTPUT_NODE), so each
workflow terminates in a built-in `PreviewAny` node wired to the STRING
(or INT) output under test; `PreviewAny` is the OUTPUT_NODE that drives
execution and surfaces the stringified value in `/history`. A separate
pass also checks every node's live `/object_info` category (see
`_check_categories`).

Usage:
    1. Start ComfyUI locally with this repo mounted under custom_nodes/.
       (Default: http://127.0.0.1:8188 — override with --host.)
    2. From repo root: `make integration` (or `python -m tests.integration.run`).

Workflow inputs are auto-normalized: any required/optional field
declared on a node's INPUT_TYPES that is missing from the workflow JSON
gets filled with the field's `default` value (when present). Practical
effect: workflows can omit the dozens of `"foo": false` boolean rows on
tag-toggle nodes and only spell out the True ones. The runner walks
`nodes.tags.*` / `nodes.text.*` once to discover NODE_CLASS_MAPPINGS.

Exits non-zero if any workflow fails to execute or any expectation is
unmet. Intentionally stdlib-only — no extra dependencies.
"""

from __future__ import annotations

import argparse
import importlib
import json
import pkgutil
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Any

_DEFAULT_HOST = "http://127.0.0.1:8188"
_POLL_INTERVAL = 0.5
_TIMEOUT = 60.0


def _build_node_registry() -> dict[str, type]:
    """Walk nodes.tags.* and nodes.text.* and collect NODE_CLASS_MAPPINGS.

    Mirrors what the package's top-level __init__.py does for ComfyUI,
    but locally — the top-level __init__.py lives in a hyphenated
    directory and isn't importable as a regular package.
    """
    registry: dict[str, type] = {}
    import nodes

    for _f, name, ispkg in pkgutil.walk_packages(nodes.__path__, nodes.__name__ + "."):
        if ispkg or name.rsplit(".", 1)[1].startswith("_"):
            continue
        try:
            mod = importlib.import_module(name)
        except Exception:
            continue
        mappings = getattr(mod, "NODE_CLASS_MAPPINGS", {})
        registry.update(mappings)
    return registry


_NODE_REGISTRY = _build_node_registry()


def _input_defaults(class_type: str) -> dict[str, Any]:
    """Return {input_name: default} for any field on the node's
    INPUT_TYPES that declares one. Missing inputs in workflow JSON get
    filled with these so users don't have to spell out every `false`."""
    cls = _NODE_REGISTRY.get(class_type)
    if cls is None:
        return {}
    input_types = getattr(cls, "INPUT_TYPES", None)
    if input_types is None:
        return {}
    try:
        spec = input_types()
    except Exception:
        return {}
    out: dict[str, Any] = {}
    for section in ("required", "optional"):
        for name, decl in (spec.get(section) or {}).items():
            # decl is typically (TYPE_NAME, {"default": ...}) or (CHOICES, {...}).
            if not isinstance(decl, tuple) or len(decl) < 2:
                continue
            meta = decl[1]
            if isinstance(meta, dict) and "default" in meta:
                out[name] = meta["default"]
    return out


def _normalize_workflow(workflow: dict[str, Any]) -> dict[str, Any]:
    """Fill missing input keys with each node's declared defaults."""
    normalised: dict[str, Any] = {}
    for node_id, node in workflow.items():
        ct = node.get("class_type", "")
        inputs = dict(node.get("inputs", {}))
        for name, default in _input_defaults(ct).items():
            inputs.setdefault(name, default)
        normalised[node_id] = {**node, "inputs": inputs}
    return normalised


def _post_json(url: str, payload: dict[str, Any]) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))  # type: ignore[no-any-return]


def _get_json(url: str) -> dict[str, Any]:
    with urllib.request.urlopen(url) as resp:
        return json.loads(resp.read().decode("utf-8"))  # type: ignore[no-any-return]


def _submit(host: str, workflow: dict[str, Any], client_id: str) -> str:
    resp = _post_json(f"{host}/prompt", {"prompt": workflow, "client_id": client_id})
    return str(resp["prompt_id"])


def _wait(host: str, prompt_id: str) -> dict[str, Any]:
    deadline = time.monotonic() + _TIMEOUT
    while time.monotonic() < deadline:
        history = _get_json(f"{host}/history/{prompt_id}")
        if prompt_id in history:
            return history[prompt_id]  # type: ignore[no-any-return]
        time.sleep(_POLL_INTERVAL)
    raise TimeoutError(f"prompt {prompt_id} did not complete in {_TIMEOUT}s")


def _check_one(host: str, case: dict[str, Any], client_id: str) -> tuple[bool, str]:
    name = case["name"]
    workflow = _normalize_workflow(case["workflow"])
    expectations: list[tuple[str, str]] = [(n, s) for n, s in case["expect"]]

    try:
        prompt_id = _submit(host, workflow, client_id)
    except urllib.error.HTTPError as e:
        return False, f"{name}: submit failed ({e.code}): {e.read().decode('utf-8', errors='replace')}"
    except (urllib.error.URLError, ConnectionError) as e:
        return False, f"{name}: cannot reach ComfyUI at {host}: {e}"

    try:
        history = _wait(host, prompt_id)
    except TimeoutError as e:
        return False, f"{name}: {e}"

    status = history.get("status", {})
    if status.get("status_str") == "error":
        return False, f"{name}: workflow execution error: {status}"

    outputs = history.get("outputs", {})
    for node_id, expected in expectations:
        node_output = outputs.get(node_id)
        if not node_output:
            return False, f"{name}: node {node_id} produced no output (outputs={list(outputs)})"
        texts = [str(t) for t in node_output.get("text", [])]
        if expected not in texts:
            return False, f"{name}: node {node_id} missing exact match for {expected!r} (got: {texts!r})"

    return True, name


def _check_categories(host: str) -> tuple[bool, str]:
    """Assert every registered node's live ComfyUI category matches the
    category derived locally from its class.

    ComfyUI loads this pack under its (hyphenated) directory name as the
    top-level package, so a node's `__module__` is prefixed
    (`comfyui-utility-nodes.nodes.tags...`) compared with the bare
    `nodes.tags...` the local registry sees. `category_for_module` must
    resolve both identically; this check is the only thing that exercises
    the *prefixed* path on a real ComfyUI — a regression there silently
    collapsed every node to the bare `UtilityNodes` root, which the
    text-output checks never noticed.
    """
    try:
        info = _get_json(f"{host}/object_info")
    except (urllib.error.URLError, ConnectionError) as e:
        return False, f"categories: cannot reach ComfyUI at {host}: {e}"

    mismatches: list[str] = []
    for class_type, cls in sorted(_NODE_REGISTRY.items()):
        expected = getattr(cls, "CATEGORY", None)
        node_info = info.get(class_type)
        if node_info is None:
            mismatches.append(f"{class_type}: not registered on ComfyUI")
            continue
        actual = node_info.get("category")
        if actual != expected:
            mismatches.append(f"{class_type}: category {actual!r} != expected {expected!r}")

    if mismatches:
        return False, "categories: " + "; ".join(mismatches)
    return True, f"categories: {len(_NODE_REGISTRY)} nodes match"


def _check_search_aliases(host: str) -> tuple[bool, str]:
    """Assert each source node's live `/object_info` search_aliases match the
    locally declared SEARCH_ALIASES (issue #22)."""
    try:
        info = _get_json(f"{host}/object_info")
    except (urllib.error.URLError, ConnectionError) as e:
        return False, f"search_aliases: cannot reach ComfyUI at {host}: {e}"

    mismatches: list[str] = []
    checked = 0
    for class_type, cls in sorted(_NODE_REGISTRY.items()):
        expected = list(getattr(cls, "SEARCH_ALIASES", []) or [])
        if not expected:
            continue
        checked += 1
        node_info = info.get(class_type)
        if node_info is None:
            mismatches.append(f"{class_type}: not registered on ComfyUI")
            continue
        actual = node_info.get("search_aliases") or []
        if actual != expected:
            mismatches.append(f"{class_type}: search_aliases mismatch (len {len(actual)} != {len(expected)})")

    if mismatches:
        return False, "search_aliases: " + "; ".join(mismatches)
    return True, f"search_aliases: {checked} source nodes match"


_KEY_PREFIX = "UtilityNodes"


def _check_node_replacements(host: str) -> tuple[bool, str]:
    """Assert every prefixed class_type registered an old->new node replacement
    so legacy workflows (saved with the bare pre-prefix names) auto-upgrade on
    load. The package's __init__ registers `<bare> -> UtilityNodes<bare>` for
    all nodes; verify each shows up in the live `/node_replacements` table."""
    try:
        table = _get_json(f"{host}/node_replacements")
    except (urllib.error.URLError, ConnectionError) as e:
        return False, f"node_replacements: cannot reach ComfyUI at {host}: {e}"

    mismatches: list[str] = []
    checked = 0
    for new_id in sorted(_NODE_REGISTRY):
        if not new_id.startswith(_KEY_PREFIX):
            mismatches.append(f"{new_id}: class_type is not {_KEY_PREFIX}-prefixed")
            continue
        old_id = new_id[len(_KEY_PREFIX) :]
        checked += 1
        entries = table.get(old_id)
        if not entries:
            mismatches.append(f"{old_id}: no replacement registered")
            continue
        if not any(e.get("new_node_id") == new_id for e in entries):
            mismatches.append(f"{old_id}: replacement does not map to {new_id}")

    if mismatches:
        return False, "node_replacements: " + "; ".join(mismatches)
    return True, f"node_replacements: {checked} legacy names auto-migrate"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default=_DEFAULT_HOST, help=f"ComfyUI base URL (default {_DEFAULT_HOST})")
    parser.add_argument(
        "--workflows",
        type=Path,
        default=Path(__file__).parent / "workflows.json",
        help="path to workflows.json",
    )
    args = parser.parse_args()

    cases = json.loads(args.workflows.read_text(encoding="utf-8"))
    client_id = str(uuid.uuid4())

    passed = 0
    failed: list[str] = []

    checks = (_check_categories, _check_search_aliases, _check_node_replacements)
    for check in checks:
        ok, msg = check(args.host)
        if ok:
            print(f"PASS  {msg}")
            passed += 1
        else:
            print(f"FAIL  {msg}")
            failed.append(msg)

    for case in cases:
        ok, msg = _check_one(args.host, case, client_id)
        if ok:
            print(f"PASS  {msg}")
            passed += 1
        else:
            print(f"FAIL  {msg}")
            failed.append(msg)

    total = len(cases) + len(checks)
    print(f"\n{passed}/{total} checks passed")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
