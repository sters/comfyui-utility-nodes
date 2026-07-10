# Act Preset

`UtilityNodes/TagMaster` menu tree. Emits a curated SFW act bundle packaging related action / posture / hand pose / expression tags into one coherent activity. Designed to layer on top of `Situation` (for the location backdrop) and `Character Preset` (for visuals) through `TagsBuild`.

Unlike the single-toggle `Body: Action` / `Body: Posture` / `Hands: Gesture` nodes, each preset here combines several tags that naturally belong together for a specific activity. Use this when the activity is the focus; add a `Situation` for the backdrop if needed.

## Inputs

- `act` (combo): select a preset from the list.
- `extra` (STRING, multiline, optional).

## Outputs

- `bundle` (CUUN_TAGS): wire into `TagsBuild`.
