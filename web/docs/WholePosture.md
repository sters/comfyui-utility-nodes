# Body: Posture (standing/lying/leaning)

Tag-toggle node under the `utility/text` category.
**Mutex node** — only one of the toggled tags survives after `TagsMerge`.
Internal layer / category: `anatomy` / `body.pose.posture`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `standing`
- `sitting`
- `lying`
- `on_back`
- `on_side`
- `on_stomach`
- `prone`
- `supine`
- `all_fours`
- `crawling`
- `crouching`
- `leaning_forward`
- `leaning_back`
- `leaning_to_the_side`
- `arched_back`
- `bent_over`
- `bending_forward`
- `jumping`
- `running`
- `walking`
- `stretching`
- `dynamic_pose`
- `contrapposto`
- `fetal_position`
- `yoga_pose`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
