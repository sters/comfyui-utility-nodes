# Hands: Pose

Tag-toggle node under the `utility/text` category.
Internal layer / category: `anatomy` / `body.hands.pose`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `preset` (combo): `custom` (use the checkboxes), `all_on`, `all_off`, `invert`.
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `prompt` (STRING): selected tags joined by `separator`.
- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `hand_up`
- `hands_up`
- `arm_up`
- `arms_up`
- `arm_behind_back`
- `arms_behind_back`
- `arm_behind_head`
- `arms_behind_head`
- `arm_at_side`
- `arm_support`
- `outstretched_arm`
- `outstretched_arms`
- `crossed_arms`
- `hand_on_own_hip`
- `hand_on_own_chest`
- `hand_on_own_face`
- `hand_to_own_mouth`
- `hand_on_another's_head`
- `hand_in_pocket`
- `own_hands_together`
- `holding_hands`
- `interlocked_fingers`
- `finger_to_mouth`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
- The `prompt` output is convenient when you only need this one node and want to drop it straight into a `TextConcat`.
