# List Shuffle

`UtilityNodes/Text` category. Shuffles a STRING list with a seed and optionally keeps only the first N items. Typically chained after `Prompt Combinator` to realize "expand all combinations, then sample N at random."

## Inputs

- `items` (STRING list): wire from an upstream list-producing node.
- `seed` (INT): random seed (deterministic for a fixed seed).
- `limit` (INT): `0` keeps everything; `>0` caps the result to that many leading items after shuffling.

## Outputs

- `items` (STRING list): shuffled (and optionally truncated) list.
