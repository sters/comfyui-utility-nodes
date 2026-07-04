# Set Metadata

`UtilityNodes/Image` category. Builds a `CUUN_METADATA` bundle one key/value pair at a time. Chain several of these — each takes an optional upstream `metadata` bundle and appends its own pair — to build up the set that [Save Image with Metadata](UtilityNodesSaveImageWithMetadata.md) embeds.

## Inputs

- `key` (STRING): the metadata key.
- `value` (STRING): the metadata value.
- `metadata` (CUUN_METADATA, optional): an upstream bundle to extend.

## Outputs

- `metadata` (CUUN_METADATA): the upstream pairs plus this node's `key`/`value`, in order.

## Notes

- Duplicate keys resolve last-write-wins — the pair added by the node closest to `Save Image with Metadata` in the chain wins.
- With no `metadata` input, the output is just this node's single pair.
