# NSFW: Position

Tag-toggle node under the `utility/text` category.
**Mutex node** — only one of the toggled tags survives after `TagsMerge`.
Internal layer / category: `nsfw_act` / `nsfw.position`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `missionary`
- `cowgirl_position`
- `reverse_cowgirl_position`
- `doggystyle`
- `anal_doggystyle`
- `mating_press`
- `prone_bone`
- `piledriver_(sex)`
- `standing_sex`
- `suspended_congress`
- `leg_lock`
- `full_nelson`
- `side-by-side`
- `spooning`
- `lotus_position`
- `carrying_sex`
- `wall_slam`
- `doggystyle_(animal)`
- `threesome`
- `foursome`
- `gangbang`
- `orgy`
- `mmf_threesome`
- `ffm_threesome`
- `mmm_threesome`
- `fff_threesome`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
