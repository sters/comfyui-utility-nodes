# Seed

`UtilityNodes/Util` menu tree. A single shared seed value (issue #20).

One `seed` INT widget with ComfyUI's **control after generate**
(fixed / increment / decrement / randomize), wired out to multiple consumers
so they all advance from the same number instead of each carrying its own
independent seed.

## Inputs

- `seed` (INT, `control_after_generate`): the seed. The little control under the widget decides what happens to it after each queue — leave it on `randomize` for fresh images, or `fixed` to reproduce one.

## Outputs

- `seed` (INT): the same value, for wiring into any INT seed socket.

## Why

A typical graph has several nodes that take a seed — `KSampler`, `TagsShuffle`,
`TagsRandomPick`, … Give them their own seeds and they drift out of sync, so a
"same image but reshuffle the tag order" tweak is fiddly. Drive them all from
one `Seed` node and a single control governs the whole graph.

```
Seed (control: randomize) ─┬─► KSampler.seed
                           ├─► TagsShuffle.seed
                           └─► TagsRandomPick.seed
```
