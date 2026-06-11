# Clothing: Hand & Arm

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
Internal layer / category: `clothing` / `clothing.hand_arm`.

## Inputs

- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `gloves`
- `fingerless_gloves`
- `half_gloves`
- `elbow_gloves`
- `mittens`
- `single_glove`
- `mismatched_gloves`
- `arm_warmers`
- `wrist_cuffs`
- `wristband`
- `sweatband`
- `bracelet`
- `bangle`
- `watch`
- `wristwatch`
- `ring`
- `armlet`
- `armband`
- `shoulder_armor`
- `pauldron`
- `vambraces`
- `gauntlets`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
