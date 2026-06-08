# Clothing: Headwear

Tag-toggle node under the `utility/text` category.
**Mutex node** — only one of the toggled tags survives after `TagsMerge`.
Internal layer / category: `clothing` / `clothing.headwear`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `hat`
- `baseball_cap`
- `beret`
- `cap`
- `peaked_cap`
- `newsboy_cap`
- `flat_cap`
- `fedora`
- `top_hat`
- `bowler_hat`
- `mob_cap`
- `sun_hat`
- `straw_hat`
- `witch_hat`
- `wizard_hat`
- `santa_hat`
- `party_hat`
- `nurse_cap`
- `police_hat`
- `military_hat`
- `helmet`
- `bicycle_helmet`
- `motorcycle_helmet`
- `hood`
- `hooded_jacket`
- `hooded_cape`
- `headphones`
- `headset`
- `earmuffs`
- `headband`
- `head_wreath`
- `head_scarf`
- `veil`
- `crown`
- `mini_crown`
- `tiara`
- `hat_ribbon`
- `hat_bow`
- `hat_flower`
- `hat_feather`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
