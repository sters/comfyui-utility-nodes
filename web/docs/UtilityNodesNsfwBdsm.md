# NSFW: BDSM

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
Internal layer / category: `nsfw_act` / `nsfw.bdsm`.

## Inputs

- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

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
