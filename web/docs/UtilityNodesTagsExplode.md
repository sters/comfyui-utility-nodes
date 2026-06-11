# Tags: Explode (per-tag axis)

`UtilityNodes/TagMaster` menu tree. Splits a `CUUN_TAGS` bundle into a **list of single-tag bundles**, one per selected tag. Designed as the adapter that turns a tag-toggle node (e.g. `HairColor` with 4 colors checked) into an axis for `TagsCombinator`.

## Inputs

- `bundle` (CUUN_TAGS): output from any tag-toggle node (or a preset).

## Outputs

- `bundles` (CUUN_TAGS list, `OUTPUT_IS_LIST=True`): one single-tag bundle per tag in the input. The original `category` / `layer` / `mutex_within` metadata is preserved on each emitted selection, so `TagsMerge` still enforces conflict rules per value downstream.

## Behavior

- Tags in the `extra` category are dropped (they're free-form text, not axis material).
- An empty input bundle emits a single empty-bundle sentinel — keeps `TagsCombinator`'s Cartesian-product math sane (the empty axis contributes one "no-op" value rather than zeroing the product).

## Typical wiring

```
HairColor(red, blue, green, black) ─→ TagsExplode ─→ TagsCombinator.axis_2
```

For preset axes that should stay as one value, **skip `TagsExplode`** and wire the preset directly into the combinator's axis socket.
