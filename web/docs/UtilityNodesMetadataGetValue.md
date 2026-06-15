# Get Metadata Value

`UtilityNodes/Image` category. Pulls a **single value by key** out of a formatted metadata dump, so you don't have to consume the whole block. Wire it after [Load Image with Metadata](UtilityNodesLoadImageWithMetadata.md) or [Extract Image Metadata](UtilityNodesExtractImageMetadata.md) (both emit `key: value` lines), or paste a dump directly.

## Inputs

- `metadata` (STRING): a `key: value` dump (one pair per line) — typically wired from Load/Extract.
- `key` (STRING): the key to read (exact match, surrounding whitespace trimmed). Examples: `seed`, `author`, `prompt`, `size`.
- `default` (STRING, optional): returned when the key is absent.

## Outputs

- `value` (STRING): the looked-up value, or `default` if the key isn't present.
- `found` (BOOLEAN): whether the key existed — lets you branch on a miss instead of guessing from `value`.

## Notes

- Each line is split on the **first** `": "`, so values may freely contain `:`, `=`, and further `": "` pairs (timestamps, URLs, embedded JSON).
- Pairs with the save round-trip: `Save Image with Metadata → Extract Image Metadata → Get Metadata Value` recovers any key you embedded.
