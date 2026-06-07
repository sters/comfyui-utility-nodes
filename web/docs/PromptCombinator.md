# Prompt Combinator

`utility/text` category. Expands a template against axis definitions into every combination of prompts. Output is a STRING list (`OUTPUT_IS_LIST=True`), so any downstream `CLIPTextEncode` / `KSampler` / `SaveImage` runs once per element automatically.

## Inputs

- `template` (STRING, multiline): template with `{name}` placeholders.
- `axes` (STRING, multiline): one axis per line in the form `name: v1, v2, v3`. Lines starting with `#` and blank lines are ignored.
- `delimiter` (STRING): separator between axis values. Escape sequences like `\n` are honored.

## Outputs (all lists)

- `prompt` (STRING): each expanded prompt.
- `label` (STRING): `name=value__...` identifier — handy as `SaveImage` `filename_prefix`.
- `index` (INT): 0-based counter.

## Example

```
template: {hair} hair, {eye} eyes
axes:
  hair: short, long
  eye: red, blue
```

→ 4 prompts (`short hair, red eyes`, `short hair, blue eyes`, `long hair, red eyes`, `long hair, blue eyes`) flow downstream.

## Tips

- Pair with `List Shuffle` to draw N random elements out of the full combination space (deterministic with `seed`).
- Use `#` comments inside the `axes` block to keep variants around without expanding them.
