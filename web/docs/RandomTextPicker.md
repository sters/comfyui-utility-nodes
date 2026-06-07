# Random Text Picker

`utility/text` category. Splits a text by a delimiter and randomly picks N items. Useful for "pick K random tags from this pool" workflows.

## Inputs

- `text` (STRING, multiline): source text.
- `delimiter` (STRING): split character. Escape sequences like `\n` and `\t` are honored.
- `count` (INT): how many items to draw. If larger than the available items, returns all of them.
- `seed` (INT): random seed (deterministic for a fixed seed).

## Outputs

- `text` (STRING): the picked items rejoined with the same delimiter.
