# NSFW: BDSM

Tag-toggle node under the `utility/text` category.
Internal layer / category: `nsfw_act` / `nsfw.bdsm`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `preset` (combo): `custom` (use the checkboxes), `all_on`, `all_off`, `invert`.
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `prompt` (STRING): selected tags joined by `separator`.
- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `bdsm`
- `bondage`
- `restrained`
- `arms_behind_back`
- `tied_up`
- `rope`
- `shibari`
- `suspension_bondage`
- `handcuffs`
- `shackles`
- `chained`
- `leash`
- `ball_gag`
- `ring_gag`
- `gag`
- `tape_gag`
- `spanking`
- `hair_pull`
- `choking`
- `torture`
- `humiliation`
- `slave`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
- The `prompt` output is convenient when you only need this one node and want to drop it straight into a `TextConcat`.
