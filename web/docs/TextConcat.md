# Text Concat

`utility/text` category. Joins up to 10 STRING inputs with `separator`. `None` and empty-string inputs are skipped, so unwired sockets and blank prompts vanish cleanly.

## Inputs

- `separator` (STRING): joiner. Escape sequences like `\n` are honored.
- `text_1` ... `text_10` (STRING, optional): only the connected ones are used.

## Outputs

- `text` (STRING): the joined string.
