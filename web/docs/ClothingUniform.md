# Clothing: Uniform & Costume

Tag-toggle node under the `utility/text` category.
**Mutex node** — only one of the toggled tags survives after `TagsMerge`.
Internal layer / category: `clothing` / `clothing.uniform`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `preset` (combo): `custom` (use the checkboxes), `all_on`, `all_off`, `invert`.
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `prompt` (STRING): selected tags joined by `separator`.
- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `school_uniform`
- `serafuku`
- `sailor_collar`
- `sailor_dress`
- `blazer_uniform`
- `gym_uniform`
- `business_suit`
- `suit`
- `pant_suit`
- `skirt_suit`
- `military_uniform`
- `uniform`
- `maid`
- `waitress`
- `nurse`
- `police_uniform`
- `cheerleader`
- `miko`
- `nun`
- `kunoichi`
- `witch`
- `santa_costume`
- `bunny_girl`
- `playboy_bunny`
- `ninja`
- `armor`
- `dougi`
- `track_suit`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
- The `prompt` output is convenient when you only need this one node and want to drop it straight into a `TextConcat`.
