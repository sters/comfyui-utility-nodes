# Bad: Body

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
All tags default to **ON** (use `invert` or the individual toggles to turn things off).
Internal layer / category: `bad` / `bad.body`.

## Inputs

- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `True`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `bad_torso`
- `bad_ass`
- `extra_pectorals`
- `extra_nipples`
- `extra_breasts`
- `extra_tails`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
