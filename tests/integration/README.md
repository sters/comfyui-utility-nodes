# Integration check

Posts a few small workflows to ComfyUI's `/prompt` endpoint and asserts the
expected text appears in each node's OUTPUT_NODE preview. Verifies the
ComfyUI plumbing (node registration, socket types, executor) works
end-to-end — complementing the offline pytest suite, which only exercises
the Python objects.

Scope is **text nodes only** (no KSampler / model loading). Intended to
run locally on demand, not in CI.

## Run

```sh
make integration
```

This builds a CPU-only ComfyUI Docker image (~1.5 GB on first build,
cached after), starts it with this repo mounted as a custom node, runs
the workflow checks, and tears the container down.

Lower-level targets:

- `make integration-up` — bring the container up and wait for healthy
- `make integration-down` — tear it down
- `make integration-logs` — tail recent ComfyUI logs

To run the checks against an existing ComfyUI (not the Docker one), skip
`integration-up` and pass a host:

```sh
uv run python -m tests.integration.run --host http://127.0.0.1:8188
```

The runner is stdlib-only — no extra Python dependencies.

## Adding cases

Edit `workflows.json`. Each entry is:

```json
{
  "name": "short_id",
  "description": "what this verifies",
  "workflow": { "<node_id>": { "class_type": "...", "inputs": {...} } },
  "expect": [["<node_id>", "substring"], ...]
}
```

The `workflow` block is the ComfyUI **API format** (the same shape the
"Save (API Format)" UI export produces). Each `expect` pair checks that
`substring` appears in the named node's `outputs.text` from the
`/history/<prompt_id>` response — which means the asserted node must
have `OUTPUT_NODE = True`. All tag-toggle nodes, `TagsMerge`,
`TagDecorate`, and `PonyPromptBuilder` qualify; pure pipe-through text
nodes (e.g. `TextConcat`) don't expose preview text, so route them
through an OUTPUT_NODE terminator if you need to assert on them.
