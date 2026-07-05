# Tags: Select (one combination by index)

`UtilityNodes/TagMaster` menu tree. Picks **one** bundle out of a `TagsCombinator` list by `index`, returning a single `CUUN_TAGS` bundle (width 1) plus its label. This is the memory-safe way to run a large sweep.

## Why this exists

Feeding a `TagsCombinator` list straight into the image pipeline fans **all** combinations out in a single Run. ComfyUI processes list-broadcast node-by-node, materialising the whole list at each stage — so a 3 × 10 × 10 = 300 sweep holds 300 decoded images **and** 300 detailer outputs (plus latents / conditioning) in memory at once. Model weights (VRAM) are fine — they're loaded once and reused across iterations — but the accumulated intermediate **tensors** (system RAM) overflow at large N.

`TagsSelect` flips the strategy from "one Run, N-wide" to "N Runs, 1-wide":

```
Seed(control_after_generate=increment) ─► index
                                            │
Combinator.bundle (list) ──────────────────┤
Combinator.label  (list) ──────────────► TagsSelect ─► bundle ─► TagsBuild ─► CLIP ─► KSampler ─► … (width 1)
                                                     ─► label  ─► (SaveImage filename_prefix)
```

Queue the prompt N times. `index` increments 0, 1, 2, …; each Run resolves to a single combination, so peak memory stays at one image's worth, images are written incrementally, and a crash mid-sweep is resumable from where you left off.

## Inputs

- `index` (INT): which combination to pick. Carries `control_after_generate` (fixed / increment / decrement / randomize) so it can advance on its own, or wire a shared `Seed` node. **Wraps modulo the list length** — queuing exactly N runs walks the whole sweep once and keeps cycling beyond that.
- `bundles` (CUUN_TAGS list, optional): the `bundle` output of `TagsCombinator`.
- `labels` (STRING list, optional): the `label` output of `TagsCombinator`, so the picked combination's label comes out aligned.

## Outputs

- `bundle` (CUUN_TAGS): the single selected bundle — wire into `TagsBuild`.
- `label` (STRING): the selected combination's label (empty if `labels` is unwired). Handy for `SaveImage` `filename_prefix`.
- `index` (INT): the **effective** (wrapped) index actually used.

## Notes

- An empty / unwired `bundles` input yields an empty bundle, empty label, and index 0.
- For small sweeps (a few dozen) the plain list fanout (`Combinator → Merge → pipeline`) is simpler and fine; reach for `TagsSelect` when N is large enough that holding N intermediates at once is a problem.
