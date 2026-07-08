# Build from Rules

`UtilityNodes/TagMaster` menu tree. Expands a `rules` JSON `STRING` (from [Rules to JSON](UtilityNodesTagsRulesToJson.md)) into combination bundles — the exact same cartesian-product expansion [Tags Combinator](UtilityNodesTagsCombinator.md) performs, but sourced from JSON instead of a live graph (issue #27).

## Inputs

- `rules` (STRING, multiline, default `[]`): JSON produced by `Rules to JSON`.

## Outputs (all lists, `OUTPUT_IS_LIST=True`)

- `bundle` (CUUN_TAGS): one Spec per combination, unmerged, exactly like `TagsCombinator`'s `bundle` output — already-resolved when no axis was deferred, or a composite folding in the deferred part when one was (any axis that was a `TagsRandomPick`/`TagsRandomBundle` output, serialized as-is by `Rules to JSON` and never expanded, resolves independently per combination). Wire into `TagsBuild`.
- `label` (STRING): per-combination identifier, same scheme as `TagsCombinator`'s `label`.
- `index` (INT): 0-based counter.

## Notes

- Malformed or empty `rules` yields no combinations (`([], [], [])`), not an error.
- Rules JSON produced before the bundle unification (no `"kind"` key per axis entry), or before `bundle_choice` candidates became nested Specs, is rejected with a clear `ValueError` rather than silently misinterpreted — regenerate it with the current `Rules to JSON`.
- Conflict resolution (`TAG_CONFLICTS` / `MUTEX_GROUPS`) is still the downstream `TagsBuild`'s job, per combination.
