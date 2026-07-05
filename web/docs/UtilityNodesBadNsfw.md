# Bad: NSFW

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
All tags default to **ON** (use `invert` or the individual toggles to turn things off).
Internal layer / category: `bad` / `bad.nsfw`.

## Inputs

- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `True`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsBuild` (carries category + mutex metadata).

## Tags

- `bad_vulva`
- `extra_penises`
- `extra_testicles`
- `extra_pussies`
- `extra_clitorises`
- `extra_anus`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsBuild` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
