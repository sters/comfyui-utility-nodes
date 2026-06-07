# Meta: Pony

`utility/text` category. Pony Diffusion V6 XL meta-template — emits the model-specific score / rating / source tags as a CUUN_TAGS bundle. Sibling to `MetaQuality`, which does the generic-quality version of the same job.

## Inputs

- `separator` (STRING).
- `score_9` ... `score_4_up` (BOOLEAN): toggle each score tag individually. Useful for keeping only the high ones in positive prompts, or only the low ones in negative prompts.
- `rating` (combo): `none` / `safe` / `questionable` / `explicit`.
- `source` (combo): `none` / `pony` / `furry` / `cartoon` / `anime`.
- `extra` (STRING, multiline, optional): body text appended after the standard tags.

## Outputs

- `prompt` (STRING): assembled in the order `score → rating → source → extra` (matching the model's recommended template).
- `bundle` (CUUN_TAGS): the same tags as a single `TaggedSelection` at category `meta.pony`, layer `meta`. Wire it into `TagsMerge` alongside `CharacterPreset` / `MetaQuality` / etc. so the standard merge / conflict / decoration pipeline keeps working downstream.

The node has `OUTPUT_NODE = True`, so the assembled result also previews under the node after running Queue Prompt.
