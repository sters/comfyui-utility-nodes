# Build from Rules

`UtilityNodes/TagMaster` menu tree. Expands a `rules` JSON `STRING` (from [Rules to JSON](UtilityNodesTagsRulesToJson.md)) into combination bundles — the exact same cartesian-product expansion [Tags Combinator](UtilityNodesTagsCombinator.md) performs, but sourced from JSON instead of a live graph (issue #27).

## Inputs

- `rules` (STRING, multiline, default `[]`): JSON produced by `Rules to JSON`.

## Outputs (all lists, `OUTPUT_IS_LIST=True`)

- `bundle` (CUUN_TAGS): one concatenated bundle per combination, unmerged — wire into `TagsMerge` exactly like `TagsCombinator`'s `bundle` output.
- `label` (STRING): per-combination identifier, same scheme as `TagsCombinator`'s `label`.
- `index` (INT): 0-based counter.
- `deferred_spec` (CUUN_TAGS): same as `TagsCombinator`'s `deferred_spec` — any axis that was a `TagsRandomPick`/`TagsRandomBundle` spec (serialized as-is by `Rules to JSON`, never expanded) round-trips here and resolves independently per combination. Wire into a separate `TagsMerge.bundle_i` slot.

## Notes

- Malformed or empty `rules` yields no combinations (`([], [], [], [])`), not an error.
- Rules JSON produced before the bundle/spec unification (no `"kind"` key per axis entry) is rejected with a clear `ValueError` rather than silently misinterpreted — regenerate it with the current `Rules to JSON`.
- Conflict resolution (`TAG_CONFLICTS` / `MUTEX_GROUPS`) is still the downstream `TagsMerge`'s job, per combination.
