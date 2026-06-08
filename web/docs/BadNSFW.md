# Bad: NSFW

Tag-toggle node under the `utility/text` category.
All tags default to **ON** (use `invert` or the individual toggles to turn things off).
Internal layer / category: `bad` / `bad.nsfw`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `True`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `bad_vulva`
- `extra_penises`
- `extra_testicles`
- `extra_pussies`
- `extra_clitorises`
- `extra_anus`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
