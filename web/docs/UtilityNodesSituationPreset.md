# Situation Preset

`UtilityNodes/TagMaster` menu tree. Emits an SFW scene bundle (location + time-of-day + atmosphere + costume + simple action) for a coherent everyday situation. Designed to layer with `Character Preset` and `Personality Preset` through `TagsBuild`.

## Inputs

- `situation` (combo): `after_school_classroom`, `cherry_blossom_park`, `gym_workout`, `hot_spring`, `karaoke_room`, `kitchen_cooking`, `library_study`, `morning_routine`, `park_picnic`, `rooftop_sunset`, `school_commute_morning`, `shopping_date`, `shrine_visit`, `snowy_streetscape`, `street_snap_city`, `summer_beach`, `summer_festival`, `winter_cafe`.
- `extra` (STRING, multiline, optional).

## Outputs

- `bundle` (CUUN_TAGS): wire into `TagsBuild`. Outfit-bearing presets (e.g. `summer_beach` → `swimsuit`) trigger `TAG_CONFLICTS` against character-bundle clothing automatically.

The flat tuples live in `nodes/tags/situation_preset.py`. NSFW counterparts are in `NsfwScenePreset`.
