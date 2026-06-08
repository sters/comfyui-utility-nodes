# Subject Count: Extract

`UtilityNodes/TagMaster/Meta` menu tree. Parses Danbooru-style subject-count
tags back **out of an assembled prompt STRING** and reports a person count.
The motivating use case (issue #19) is feeding a count into a downstream
detector / segmenter such as SAM3: wire `TagsMerge.prompt` → this node →
`total`.

## Inputs

- `prompt` (STRING, multiline): the assembled prompt. Usually wired from a `TagsMerge` `prompt` output, but any text works.

## Outputs

- `count_tags` (STRING): the matched count tags, in the order found, joined by `, ` (e.g. `2girls, 1boy`).
- `total` (INT): total person count (see counting rules below).
- `girls` (INT) / `boys` (INT) / `others` (INT): per-gender counts.

## Recognised tags

- **Numbered gendered**: `1girl`, `2girls`, `3boys`, `1other`, `4others`, …
- **`+` form**: `6+girls` counts as its floor number (`6`).
- **`multiple_*`**: `multiple_girls` / `multiple_boys` / `multiple_others` — with no explicit number, contributes a floor of `2` for that gender.
- **Total-only**: `solo`, `solo_focus`, `duo`, `trio`, `couple`, `group`.

## Counting rules

- `total` = `girls + boys + others` when any gendered tag is present.
- If no gendered tag is present, `total` falls back to the highest total-only tag: `solo`/`solo_focus` → 1, `duo`/`couple` → 2, `trio` → 3.
- `group` on its own leaves `total` at `0` (the exact count is unknown — set it yourself downstream).
- Matching is word-boundary aware, so `girlfriend`, `otherwise`, and `1080p` are **not** parsed as count tags.

## Typical wiring

```
…tag nodes… ─► TagsMerge ─┬─► CLIPTextEncode ─► (your image pipeline)
                          └─► Subject Count: Extract ─► total (INT) ─► SAM3 / detector
```
