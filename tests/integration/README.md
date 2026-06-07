# Integration check

Posts a few small workflows to a **running ComfyUI instance** and asserts the
expected text appears in each node's OUTPUT_NODE preview. Verifies the
ComfyUI plumbing (node registration, socket types, executor) works
end-to-end — complementing the offline pytest suite, which only exercises
the Python objects.

Scope is **text nodes only** (no KSampler / model loading). Intended to
run locally on demand, not in CI.

## Setup

1. Install ComfyUI somewhere on the host
   ([comfy-cli](https://docs.comfy.org/comfy-cli/getting-started) is the
   easiest path).
2. Make this repo discoverable as a custom node — symlink or clone into
   `ComfyUI/custom_nodes/`:

   ```sh
   ln -s "$PWD" /path/to/ComfyUI/custom_nodes/comfyui-utility-nodes
   ```

3. Start ComfyUI (CPU is fine, no models needed):

   ```sh
   cd /path/to/ComfyUI && python main.py --cpu --listen 127.0.0.1
   ```

## Run

From the repo root:

```sh
make integration
```

Or directly:

```sh
uv run python -m tests.integration.run
```

Options:

- `--host http://127.0.0.1:8188` — override the ComfyUI URL.
- `--workflows path/to/file.json` — point at a different test definition.

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
have `OUTPUT_NODE = True`. All tag-toggle nodes, `TagsMerge`, and
`PonyPromptBuilder` qualify; pure pipe-through text nodes (e.g.
`TextConcat`, `PromptCombinator`) don't expose preview text, so route
them through an OUTPUT_NODE terminator if you need to assert on them.
