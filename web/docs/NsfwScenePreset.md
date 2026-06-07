# NSFW Scene Preset

`utility/text` category. Emits a curated NSFW scene bundle covering act / position / state / aftermath cues in one click. Designed to layer with `Character Preset` and `Personality Preset` through `TagsMerge`.

## Inputs

- `scene` (combo): `after_sex_aftermath`, `anal_focus`, `bound_submissive`, `breast_play`, `bukkake`, `cowgirl_riding`, `doggystyle`, `fellatio_pov`, `femdom_dominant`, `first_time_shy`, `footjob_dominant`, `handjob_dominant`, `lingerie_tease`, `masturbation_solo`, `mating_press`, `paizuri_scene`, `panty_shot_voyeur`, `public_exposure`, `shibari_suspension`, `shower_scene`, `squirting`, `threesome_ffm`, `vanilla_missionary`.
- `separator` (STRING).
- `extra` (STRING, multiline, optional).

## Outputs

- `prompt` (STRING).
- `bundle` (CUUN_TAGS): wire into `TagsMerge`. Clothing / nude triggers in the preset interact with regular tag nodes through `TAG_CONFLICTS` automatically.

The flat tuples live in `nodes/tags/nsfw_preset.py`.
