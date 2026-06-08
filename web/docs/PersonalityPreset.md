# Personality Preset

`utility/text` category. Emits a tag bundle that nudges the model toward a personality archetype (face / expression / pose cues — not a costume).

## Inputs

- `personality` (combo): `airhead`, `angry_fierce`, `apathetic`, `confident`, `dandere`, `genki`, `gyaru`, `hardboiled`, `kuudere`, `menhera`, `mesugaki`, `motherly`, `ojou_sama`, `playful_tease`, `scared`, `seiso`, `shy_girl`, `sleepy`, `tsundere`, `yandere`.
- `separator` (STRING).
- `extra` (STRING, multiline, optional).

## Outputs

- `bundle` (CUUN_TAGS): wire into `TagsMerge`. Layer with `Character Preset` and a Scene preset for character × mood × scene workflows.

The flat tuples live in `nodes/tags/personality.py`.
