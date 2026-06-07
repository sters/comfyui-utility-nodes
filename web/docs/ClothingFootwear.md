# Clothing: Footwear

Tag-toggle node under the `utility/text` category.
**Mutex node** — only one of the toggled tags survives after `TagsMerge`.
Internal layer / category: `clothing` / `clothing.footwear`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `preset` (combo): `custom` (use the checkboxes), `all_on`, `all_off`, `invert`.
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `prompt` (STRING): selected tags joined by `separator`.
- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `shoes`
- `sneakers`
- `loafers`
- `mary_janes`
- `high_heels`
- `stiletto_heels`
- `platform_heels`
- `platform_footwear`
- `wedge_heels`
- `pumps`
- `boots`
- `ankle_boots`
- `knee_boots`
- `thigh_boots`
- `cross-laced_footwear`
- `combat_boots`
- `rain_boots`
- `sandals`
- `flip-flops`
- `geta`
- `okobo`
- `zouri`
- `slippers`
- `uwabaki`
- `ballet_slippers`
- `cleats`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
- The `prompt` output is convenient when you only need this one node and want to drop it straight into a `TextConcat`.
