# NSFW State: Aftermath & Expression

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
Internal layer / category: `nsfw_state` / `nsfw.state.aftermath`.

## Inputs

- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsBuild` (carries category + mutex metadata).

## Tags

- `after_sex`
- `after_vaginal`
- `after_anal`
- `after_oral`
- `after_fellatio`
- `orgasm`
- `female_orgasm`
- `male_orgasm`
- `simultaneous_orgasm`
- `convulsing`
- `moaning`
- `x-ray`
- `internal_cumshot`
- `cross-section`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsBuild` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
