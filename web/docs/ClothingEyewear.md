# Clothing: Eyewear

Tag-toggle node under the `utility/text` category.
**Mutex node** — only one of the toggled tags survives after `TagsMerge`.
Internal layer / category: `clothing` / `clothing.eyewear`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `glasses`
- `sunglasses`
- `round_eyewear`
- `semi-rimless_eyewear`
- `rimless_eyewear`
- `over-rim_eyewear`
- `under-rim_eyewear`
- `goggles`
- `swim_goggles`
- `eyepatch`
- `medical_eyepatch`
- `monocle`
- `pince-nez`
- `blindfold`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
