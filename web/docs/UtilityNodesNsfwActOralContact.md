# NSFW Act: Oral & Contact

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
Internal layer / category: `nsfw_act` / `nsfw.act.oral_contact`.

## Inputs

- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `fellatio`
- `irrumatio`
- `cunnilingus`
- `paizuri`
- `handjob`
- `footjob`
- `thigh_sex`
- `kissing`
- `french_kiss`
- `breast_sucking`
- `nipple_sucking`
- `breast_grab`
- `ass_grab`
- `groping`
- `frottage`
- `tribadism`
- `autofellatio`
- `autocunnilingus`
- `licking`
- `biting`
- `bukkake`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
