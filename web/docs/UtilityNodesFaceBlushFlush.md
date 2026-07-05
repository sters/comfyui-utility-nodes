# Face: Blush & Flush

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
Internal layer / category: `anatomy` / `body.face.blush_flush`.

## Inputs

- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsBuild` (carries category + mutex metadata).

## Tags

- `blush`
- `light_blush`
- `full-face_blush`
- `embarrassed_blush`
- `nose_blush`
- `blush_stickers`
- `scribble_blush`
- `heavy_breathing`
- `panting`
- `sweatdrop`
- `trembling`
- `shaking`
- `flying_sweatdrops`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsBuild` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
