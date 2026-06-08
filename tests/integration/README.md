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
  "expect": [["<node_id>", "exact text"], ...]
}
```

The `workflow` block is the ComfyUI **API format** (the same shape the
"Save (API Format)" UI export produces). Each `expect` pair requires
that the exact string equals one of the elements of the named node's
`outputs.text` from the `/history/<prompt_id>` response — which means
the asserted node must have `OUTPUT_NODE = True`. All tag-toggle nodes,
`TagsMerge`, `TagsDecorate`, and `MetaPony` qualify; pure
pipe-through text nodes (e.g. `TextConcat`) don't expose preview text,
so route them through an OUTPUT_NODE terminator if you need to assert
on them.

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

- For a single-prompt node, write the full prompt string.
- For a list-output node (e.g. `TagsDecorate` with `INPUT_IS_LIST=True`),
  one expectation per variant you care about. Each must equal one of
  the texts in the list verbatim.

For nodes that still take a `separator` (`TagsMerge`, `TagsCombinator`,
`TextConcat`), if `inputs.separator` is omitted the default `", "` is
used, so the expectation should also use `, ` as the joiner. Every other
node joins its preview with a fixed `", "`.
