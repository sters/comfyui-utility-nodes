# Body: Action

Tag-toggle node under the `utility/text` category.
**Mutex node** — only one of the toggled tags survives after `TagsMerge`.
Internal layer / category: `anatomy` / `body.action`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `preset` (combo): `custom` (use the checkboxes), `all_on`, `all_off`, `invert`.
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `prompt` (STRING): selected tags joined by `separator`.
- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `eating`
- `drinking`
- `licking`
- `smoking`
- `reading`
- `writing`
- `drawing`
- `painting`
- `sleeping`
- `dreaming`
- `napping`
- `dancing`
- `singing`
- `playing_instrument`
- `playing_guitar`
- `playing_piano`
- `cooking`
- `baking`
- `cleaning`
- `washing`
- `bathing`
- `showering`
- `swimming`
- `diving`
- `fishing`
- `shopping`
- `studying`
- `gaming`
- `praying`
- `meditating`
- `phone_call`
- `texting`
- `selfie`
- `waving`
- `pointing`
- `carrying`
- `hugging`
- `petting`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
- The `prompt` output is convenient when you only need this one node and want to drop it straight into a `TextConcat`.
