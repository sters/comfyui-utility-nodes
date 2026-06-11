# Body: Animal Ears

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
**Mutex node** — only one of the toggled tags survives after `TagsMerge`.
Internal layer / category: `anatomy` / `body.animal.ears`.

## Inputs

- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `animal_ears`
- `cat_ears`
- `dog_ears`
- `fox_ears`
- `wolf_ears`
- `rabbit_ears`
- `bunny_ears`
- `mouse_ears`
- `horse_ears`
- `cow_ears`
- `sheep_ears`
- `bear_ears`
- `deer_ears`
- `tiger_ears`
- `lion_ears`
- `monkey_ears`
- `raccoon_ears`
- `elf_ears`
- `pointy_ears`
- `fish_ears`
- `bird_ears`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
