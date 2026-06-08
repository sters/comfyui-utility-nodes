# Body: Animal Tail

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
**Mutex node** — only one of the toggled tags survives after `TagsMerge`.
Internal layer / category: `anatomy` / `body.animal.tail`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `tail`
- `animal_tail`
- `cat_tail`
- `dog_tail`
- `fox_tail`
- `wolf_tail`
- `rabbit_tail`
- `monkey_tail`
- `horse_tail`
- `cow_tail`
- `lizard_tail`
- `snake_tail`
- `dragon_tail`
- `demon_tail`
- `devil_tail`
- `feathered_tail`
- `multiple_tails`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
