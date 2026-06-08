# Meta: Pony

`UtilityNodes/TagMaster` menu tree. Pony Diffusion V6 XL meta-template — emits the model-specific score / rating / source tags as a CUUN_TAGS bundle. Sibling to `MetaQuality`, which does the generic-quality version of the same job.

## Inputs

- `separator` (STRING).
- `score_9` ... `score_4_up` (BOOLEAN, default `True`): toggle each score tag individually. Useful for keeping only the high ones in positive prompts, or only the low ones in negative prompts.
- `rating_safe` / `rating_questionable` / `rating_explicit` (BOOLEAN, default `False`): pick the rating tags you want (multi-select; turn them all off for none).
- `source_pony` / `source_furry` / `source_cartoon` / `source_anime` (BOOLEAN, default `False`): pick the source tags the same way.
- `extra` (STRING, multiline, optional): body text appended after the standard tags.

## Outputs

- `bundle` (CUUN_TAGS): selected tags as a single `TaggedSelection` at category `meta.pony`, layer `meta`, in the order `score → rating → source`, with any `extra` appended as its own `extra` selection. Wire it into `TagsMerge` alongside `CharacterPreset` / `MetaQuality` / etc. so the standard merge / conflict / decoration pipeline keeps working downstream.

The node has `OUTPUT_NODE = True`, so the assembled result also previews under the node after running Queue Prompt.
