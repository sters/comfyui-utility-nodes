# Face / Eyes: State & Gaze

Tag-toggle node under the `utility/text` category.
Internal layer / category: `anatomy` / `body.face.eyes.state`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `closed_eyes`
- `one_eye_closed`
- `half-closed_eyes`
- `narrowed_eyes`
- `wide-eyed`
- `looking_at_viewer`
- `looking_away`
- `looking_down`
- `looking_up`
- `looking_back`
- `looking_to_the_side`
- `looking_ahead`
- `looking_at_another`
- `side_glance`
- `eye_contact`
- `glaring`
- `rolling_eyes`
- `crying`
- `teary_eyes`
- `streaming_tears`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
