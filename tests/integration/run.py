"""Integration check against a running ComfyUI instance.

Reads `workflows.json`, posts each workflow to ComfyUI's `/prompt`
endpoint, polls `/history/<prompt_id>` until completion, and asserts
expected substrings appear in the OUTPUT_NODE preview text of named
nodes.

Usage:
    1. Start ComfyUI locally with this repo mounted under custom_nodes/.
       (Default: http://127.0.0.1:8188 — override with --host.)
    2. From repo root: `make integration` (or `python -m tests.integration.run`).

Exits non-zero if any workflow fails to execute or any expectation is
unmet. Intentionally stdlib-only — no extra dependencies.
"""

from __future__ import annotations

import argparse
import json
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
    workflow = case["workflow"]
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
    for node_id, needle in expectations:
        node_output = outputs.get(node_id)
        if not node_output:
            return False, f"{name}: node {node_id} produced no output (outputs={list(outputs)})"
        texts = node_output.get("text", [])
        haystack = " ".join(str(t) for t in texts)
        if needle not in haystack:
            return False, f"{name}: node {node_id} missing '{needle}' (got: {haystack!r})"

    return True, name


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
    for case in cases:
        ok, msg = _check_one(args.host, case, client_id)
        if ok:
            print(f"PASS  {msg}")
            passed += 1
        else:
            print(f"FAIL  {msg}")
            failed.append(msg)

    print(f"\n{passed}/{len(cases)} workflows passed")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
