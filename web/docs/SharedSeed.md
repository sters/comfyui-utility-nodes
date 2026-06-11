# Seed

`UtilityNodes/Util` menu tree. A single shared seed value (issue #20). Registered as the class `SharedSeed` (the menu still shows it as **Seed**) so it doesn't collide with the `Seed` node other popular packs register and get dropped from the menu — see [Why the class is `SharedSeed`](#why-the-class-is-sharedseed).

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

## Why the class is `SharedSeed`

`Seed` is a `class_type` that several widely-installed packs (rgthree, Impact Pack, …) also register. ComfyUI keeps all custom nodes in one global `NODE_CLASS_MAPPINGS` dict, so duplicate keys silently overwrite each other — whichever pack loads last wins, and the rest disappear from the Add-Node menu (issue #25). Registering under the unique key `SharedSeed` keeps this node always present; the display name stays `Seed` so search still finds it.
