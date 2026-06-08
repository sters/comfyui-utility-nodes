# Tags: Random Pick

`utility/text` category. Picks `count` random tags out of every non-`extra` selection in a CUUN_TAGS bundle, returns them as a single new selection at category `random_pick`. Use for "give me a random subset of these tags in the prompt" — variety without writing a separate template for each combination.

## Inputs

- `separator` (STRING).
- `count` (INT, ≥ 1): number of tags to sample (without replacement).
- `seed` (INT): RNG seed. Same seed = same picks.
- `bundle` (CUUN_TAGS, optional).

## Outputs

- `bundle` (CUUN_TAGS): one selection at `random_pick` / `random` with the picked tags, followed by the original `extra` selections (if any). The flattened result also previews as the node's OUTPUT_NODE preview.

## Behavior

- Tags from every non-`extra` selection are flattened into one pool before sampling. Category metadata of the source selections is lost on purpose — the picked tags live under a new `random_pick` category.
- If `count >= number of available tags`, every tag is returned (shuffled).
- `extra` selections pass through untouched.

## Typical use

Combine with a tag-toggle node to express "vary one of these N options each run":

```
ClothingPattern(plaid, checkered, polka_dot, floral_print) ─► TagsRandomPick(count=1, seed=…)
                                                              │
                                                              ▼
                                                       one random pattern per run
```

For deterministic per-image variation, wire the KSampler seed (or any other changing INT) into the `seed` input.
