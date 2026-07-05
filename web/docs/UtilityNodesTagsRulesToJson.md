# Rules to JSON

`UtilityNodes/TagMaster` menu tree. Serializes the axes you'd wire into `TagsCombinator` — the *candidates*, not the expansion — to a single JSON `STRING` (issue #27).

Wiring a heavy graph (many toggle nodes, presets, `TagsExplode`/`TagsCollect`) just to re-run the same combinatorial sweep every time is expensive to manage. Run this node once, preview/save the JSON with `PreviewAny`, and [Build from Rules](UtilityNodesTagsBuildFromRules.md) can regenerate every combination from just that string — no source graph required.

## Inputs

- `axis_1` ... `axis_8` (CUUN_TAGS, optional, `INPUT_IS_LIST=True`): identical wiring to [Tags Combinator](UtilityNodesTagsCombinator.md)'s axes — a preset, a tag-toggle node through `TagsExplode`, several whole bundles through `TagsCollect`, or a `TagsRandomPick`/`TagsRandomBundle` spec wired directly in for a deferred (random) axis.

## Outputs

- `rules` (STRING): the axes, verbatim, as JSON. A deferred axis serializes as one compact spec object (`{"kind": "tag_pick", ...}` / `{"kind": "bundle_choice", ...}`), not as N expanded candidates. Feed straight into `Build from Rules`, or save it to disk.

## Wiring

```
Workflow A (build once):
  CharacterPreset ×N ─→ TagsCollect ─┐
  HairColor ─→ TagsExplode ──────────┼─→ RulesToJson.axis_i ─→ PreviewAny (save the JSON)
  BodyFigure ─→ TagsExplode ─────────┘

Workflow B (generate any time, no source graph needed):
  BuildFromRules(rules) ─→ TagsMerge ─→ ...
```
