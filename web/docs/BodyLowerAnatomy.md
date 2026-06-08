# Body: Lower Anatomy

Tag-toggle node under the `utility/text` category.
Internal layer / category: `anatomy` / `body.lower_anatomy`.

## Inputs

- `separator` (STRING): joiner between selected tags (supports escape sequences like `\n`).
- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsMerge` (carries category + mutex metadata).

## Tags

- `ass`
- `ass_visible_through_thighs`
- `cameltoe`
- `pussy`
- `anus`
- `clitoris`
- `pubic_hair`
- `female_pubic_hair`
- `presenting`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsMerge` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
