# Clothing: Legwear

Tag-toggle node in the `UtilityNodes/TagMaster` menu tree.
**Mutex node** — only one of the toggled tags survives after `TagsBuild`.
Internal layer / category: `clothing` / `clothing.legwear`.

## Inputs

- `invert` (BOOLEAN): if `True`, every checkbox is flipped (unchecked tags get emitted, checked ones drop out).
- One BOOLEAN toggle per tag below (default: `False`).
- `extra` (STRING, optional, multiline): free-form text appended after the joined tags.

## Outputs

- `bundle` (CUUN_TAGS): structured selection for `TagsBuild` (carries category + mutex metadata).

## Tags

- `thighhighs`
- `over-the-knee_socks`
- `kneehighs`
- `socks`
- `ankle_socks`
- `loose_socks`
- `bobby_socks`
- `tabi`
- `stockings`
- `pantyhose`
- `leg_warmers`
- `single_thighhigh`
- `single_kneehigh`
- `single_sock`
- `zettai_ryouiki`
- `no_socks`
- `no_legwear`

## Notes

- For consistent prompts across multiple tag nodes, prefer wiring the `bundle` output through `TagsBuild` (it resolves cross-node conflicts via `MUTEX_GROUPS` and `TAG_CONFLICTS`).
