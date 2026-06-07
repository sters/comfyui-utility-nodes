# Tags: Bundle Inspector

`utility/text` category. Pass-through visualizer for a `CUUN_TAGS` bundle. Drop it between `TagsMerge` and `CLIPTextEncode` to see what survived the merge — and, optionally, what got dropped — in one UI box.

## Inputs

- `bundle` (CUUN_TAGS): the merged bundle to inspect.
- `warnings` (STRING, optional): wire `TagsMerge.warnings` here to render the drop log under the kept tags.

## Outputs

- `bundle` (CUUN_TAGS): the input bundle, unchanged. Inspector is inline-safe.
- `report` (STRING): the formatted summary (same text shown in the node's UI).

## Display

```
[base]
  hair_color : red_hair
  eye_color  : blue_eyes
[clothing]
  outfit     : school_uniform

--- dropped ---
mutex_group: kept 'long_skirt', dropped ['skirt']
conflict: dropped ['bottomless'] from 'outfit' (triggered by ['school_uniform'])
```

Selections are grouped by `layer` in first-seen order; within a layer, selections appear in input order so the listing mirrors the flatten order `TagsMerge` produces.
