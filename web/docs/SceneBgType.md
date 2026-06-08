# Scene: Background Type

Tag-toggle node under the `utility/text` category.
**Mutex node** — only one of the toggled tags survives after `TagsMerge`.
Internal layer / category: `scene` / `scene.bg_type`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `simple_background`
- `white_background`
- `black_background`
- `grey_background`
- `gradient_background`
- `blurry_background`
- `transparent_background`
- `abstract_background`
- `two-tone_background`
- `checkered_background`
- `floral_background`
- `striped_background`
- `dotted_background`
- `patterned_background`
- `scenery`
- `no_background`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
