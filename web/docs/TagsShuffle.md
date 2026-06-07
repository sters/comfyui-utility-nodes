# Tags: Shuffle

`utility/text` category. Randomly reorders the tags inside each `TaggedSelection` of a CUUN_TAGS bundle. Selection structure (category / layer / mutex_within) is preserved, so the downstream merge / decorate pipeline keeps working — only the textual tag order changes.

## Inputs

- `separator` (STRING).
- `seed` (INT): RNG seed. Same seed = same shuffle.
- `bundle` (CUUN_TAGS, optional).

## Outputs

- `prompt` (STRING): flattened result with the shuffled order.
- `bundle` (CUUN_TAGS): same selections as input, with each selection's `tags` tuple reordered.

## Behavior

- `extra` selections and single-tag selections are passed through untouched (nothing to shuffle).
- The shuffle is per-selection, not global. Tags from `hair.color` stay in the `hair.color` selection — they just appear in a different order. If you want a global shuffle across all categories, route through `TagsRandomPick` with a large `count` instead.

## Typical use

Reduce token-position bias in long prompts by re-shuffling after every queue. Pair with KSampler's `seed` advance to get a new shuffle per run.
