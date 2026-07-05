# Clothing: Footwear

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
**Mutex node** — only one of the toggled tags survives after `TagsBuild`.
Internal layer / category: `clothing` / `clothing.footwear`.

## Inputs

- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsBuild` (carries category + mutex metadata).

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

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsBuild` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
