# NSFW: Toy

Tag-toggle node under the `utility/text` category.
Internal layer / category: `nsfw_act` / `nsfw.toy`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `sex_toy`
- `dildo`
- `vibrator`
- `anal_beads`
- `butt_plug`
- `anal_tail`
- `huge_dildo`
- `vibrator_in_thighhighs`
- `vibrator_on_nipple`
- `vibrator_under_clothes`
- `onahole`
- `fleshlight`
- `condom`
- `used_condom`
- `egg_vibrator`
- `wand_vibrator`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
