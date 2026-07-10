# NSFW Act Preset

`UtilityNodes/TagMaster` menu tree. Emits a curated NSFW act bundle covering position / state / expression / aftermath cues in one click. Designed to layer with `Character Preset`, `Personality Preset`, and `Situation` (for the location backdrop) through `TagsBuild`.

Location is intentionally omitted — combine with a `Situation` preset for the setting (e.g. `hot_spring` situation + `vanilla_missionary` act, or `hospital_ward` situation + `breast_play` act).

## Inputs

- `act` (combo): select a preset from the list.
- `extra` (STRING, multiline, optional).

## Outputs

- `bundle` (CUUN_TAGS): wire into `TagsBuild`. Clothing / nude triggers in the preset interact with regular tag nodes through `TAG_CONFLICTS` automatically.
