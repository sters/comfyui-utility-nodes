# Integration check

Posts a few small workflows to ComfyUI's `/prompt` endpoint and asserts the
expected text appears in each terminating `PreviewAny` node's output. Also
checks every registered node's live `/object_info` **category** against the
one derived locally. Verifies the ComfyUI plumbing (node registration, menu
category, socket types, executor) works end-to-end — complementing the
offline pytest suite, which only exercises the Python objects.

This pack's own nodes are **pure data nodes** — none set `OUTPUT_NODE`, so a
graph of only our nodes has no terminator and ComfyUI won't execute it. Each
text-assertion workflow therefore ends in a built-in **`PreviewAny`** node
(`"class_type": "PreviewAny"`, single `source` input of ANY type) wired to
the STRING/INT output under test. `PreviewAny` is the OUTPUT_NODE that drives
execution and stringifies the value into `outputs.text`. Bundle-only outputs
(`CUUN_TAGS`) are routed through `TagsMerge` first to get a flat prompt
STRING.

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
  "expect": [["<node_id>", "exact text"], ...]
}
```

The `workflow` block is the ComfyUI **API format** (the same shape the
"Save (API Format)" UI export produces). Each `expect` pair requires
that the exact string equals one of the elements of the named node's
`outputs.text` from the `/history/<prompt_id>` response. Since this
pack's nodes are not OUTPUT_NODEs, the asserted node is almost always a
trailing `PreviewAny` (which stringifies whatever you wire to its
`source`). Wire the STRING you care about straight into `PreviewAny`;
for a `CUUN_TAGS` bundle, route it through `TagsMerge` first so the
flattened prompt — not the dataclass repr — is what gets stringified.

### Input defaulting

The runner walks every `TagNodeBase` subclass at startup and pulls each
input's `default` value out of `INPUT_TYPES`. Any field missing from a
workflow's `inputs` block is filled in with that default before the
workflow is submitted. Practical effect: you only have to spell out the
inputs you actually want to override.

```json
"1": {
  "class_type": "ClothingTops",
  "inputs": {"shirt": true, "blouse": true, "hoodie": true}
}
```

Equivalent to writing out every other boolean as `false`, the
`invert` toggle as `false`, etc. — but a lot shorter.

### Expectation shape

`expect` uses **exact equality** against each element of the node's
text list:

- For a single-prompt result, write the full prompt string.
- For a list output (e.g. a `TagsDecorate` bundle list flowing through a
  `TagsMerge` that runs once per element), `PreviewAny` collects one text
  per element — write one expectation per variant you care about. Each
  must equal one of the texts in the list verbatim.

For nodes that take a `separator` (`TagsMerge`, `TagsCombinator`,
`TextConcat`), if `inputs.separator` is omitted the default `", "` is
used, so the expectation should also use `, ` as the joiner.
