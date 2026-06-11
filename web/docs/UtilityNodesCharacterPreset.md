# Character Preset

`UtilityNodes/TagMaster` menu tree. Emits a curated bundle of character tags (hair / outfit / accessory / scene) for an archetype in one click. The result still goes through the standard merge pipeline, so layering with regular tag nodes resolves cleanly via `TagsMerge`.

## Inputs

- `character` (combo): preset name. Available: `blazer_schoolgirl`, `bunny_girl`, `catgirl_basic`, `cheerleader`, `gothic_lolita`, `knight`, `kunoichi`, `magical_girl`, `maid`, `miko`, `nun`, `nurse`, `office_lady`, `princess`, `santa_girl`, `serafuku_schoolgirl`, `vampire`, `witch`, `yandere_schoolgirl`, `yukata_festival`.
- `extra` (STRING, multiline, optional): free-form text appended after the preset tags.

## Outputs

- `bundle` (CUUN_TAGS): wire into `TagsMerge` to mix with other tag nodes; conflicts (hair color, outfit, etc.) get resolved there.

## Tips

- Layer a `Character Preset` with a `Personality Preset` and a Scene preset through one `TagsMerge` for "character × mood × scene" workflows. The `test_preset_combos.py` test exercises exactly that matrix.
- The flat tuples live in `nodes/tags/preset.py`; copy one and edit if you want a tweaked variant.
