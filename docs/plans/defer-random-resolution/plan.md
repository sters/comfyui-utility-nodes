# Defer random resolution to a final build step

## Context

`TagsRandomPick` / `TagsRandomBundle` currently roll their dice the moment
ComfyUI executes them — they read inputs and immediately return a *resolved*
`CUUN_TAGS` bundle, same as every deterministic tag-toggle/preset node. The
goal is for randomness to instead behave like the rest of the TagMaster
pipeline: hold the *candidates* as data, and only resolve them in one final
"build" step.

Worth noting: most of the pipeline **already works this way** for
deterministic data. `TaggedSelection` bundles from toggle nodes and presets
already flow un-resolved (conflicts/mutex are *not* applied at the source
node) all the way to `TagsMerge`, which is the single place that applies
`MUTEX_GROUPS` / `TAG_CONFLICTS` with **last-occurrence-wins** semantics
(`nodes/tags/_conflicts.py`, `nodes/tags/merge.py`). So "later input overrides
earlier" already exists today — it's `TagsMerge`'s job. The actual gap is
narrower than "redesign everything": **only the two random nodes commit to a
concrete value before the final build runs.**

This plan closes that gap by introducing a small "spec" (unresolved
candidate) type alongside the existing `TaggedSelection` ("resolved value")
type, and a new `TagsRandomBuild` node that performs the resolution —
mirroring how `TagsMerge` is already the single resolution point for
conflicts. Random nodes become producers of specs instead of producers of
resolved bundles.

Out of scope (flagged, not silently dropped): making the random *pool* itself
conflict-aware (e.g. not wasting a `TagsRandomPick` sample on a tag that
`TagsMerge` would later drop due to `nude`) would require the build step to
see the full cross-bundle context, not just its own spec. That's a real
future extension but a separate, bigger change — this plan only changes
*when* randomness is rolled, not what it's rolled against. `RandomTextPicker`
(plain-STRING node, outside the `CUUN_TAGS` pipeline) is left untouched since
there's no bundle/build pipeline for it to plug into.

## Design

### 1. New spec type — `nodes/tags/_base.py`

Add a frozen dataclass next to `TaggedSelection`:

```python
RANDOM_SPEC_TYPE = "CUUN_TAG_SPEC"

@dataclass(frozen=True)
class RandomSpec:
    """An unresolved random choice, held as data until TagsRandomBuild resolves it."""
    kind: Literal["bundle_choice", "tag_pick"]
    seed: int
    bundles: tuple[tuple[TaggedSelection, ...], ...] = ()  # bundle_choice candidates
    pool: tuple[TaggedSelection, ...] = ()                  # tag_pick source bundle
    count: int = 1                                           # tag_pick sample size
```

### 2. `TagsRandomBundle` (`nodes/tags/random_bundle.py`) and `TagsRandomPick` (`nodes/tags/random_pick.py`)

Change `RETURN_TYPES` from `(TAGS_TYPE,)` to `(RANDOM_SPEC_TYPE,)`, rename the
output to `spec`, and change their `pick` methods to *construct and return a
`RandomSpec`* instead of calling `random.Random(...)` themselves. No
randomness happens in these nodes anymore — they just package the candidates
they were wired.

### 3. New node — `nodes/tags/random_build.py` → `TagsRandomBuild`

The resolver. Takes up to 10 `spec_i` (`CUUN_TAG_SPEC`, optional) inputs,
resolves each with `random.Random(spec.seed)` (logic lifted verbatim from the
current `pick` bodies — pure move, no behavior change in the resolved
output), concatenates the resolved selections, and emits one `CUUN_TAGS`
`bundle` output. Wire it exactly where the random nodes used to feed
`TagsMerge` directly — `TagsRandomBundle`/`TagsRandomPick` → `TagsRandomBuild`
→ `TagsMerge`.

```python
RETURN_TYPES: ClassVar[tuple[str, ...]] = (TAGS_TYPE,)
RETURN_NAMES: ClassVar[tuple[str, ...]] = ("bundle",)
FUNCTION = "build"
CATEGORY = "UtilityNodes/TagMaster"
```

Resolution helper (module-level, used by `build`):

```python
def _resolve(spec: RandomSpec) -> tuple[TaggedSelection, ...]:
    rng = random.Random(spec.seed)
    if spec.kind == "bundle_choice":
        return rng.choice(spec.bundles) if spec.bundles else ()

    pool: list[str] = []
    extras: list[TaggedSelection] = []
    for sel in spec.pool:
        if sel.category == "extra":
            extras.append(sel)
        else:
            pool.extend(sel.tags)

    n = min(spec.count, len(pool))
    picked = rng.sample(pool, n) if n else []
    out: list[TaggedSelection] = []
    if picked:
        out.append(TaggedSelection(category="random_pick", layer="random", tags=tuple(picked), mutex_within=False))
    out.extend(extras)
    return tuple(out)
```

(This is exactly the body currently inside `TagsRandomPick.pick` /
`TagsRandomBundle.pick` — moved, not rewritten.)

### 4. Tests

- `tests/tags/test_random_pick.py` / `test_random_bundle.py`: assert the
  returned `RandomSpec` fields (kind/seed/pool/count or bundles) instead of
  resolved tags.
- New `tests/tags/test_random_build.py`: feed hand-built `RandomSpec`s through
  `TagsRandomBuild.build` and assert the resolved bundle matches
  `random.Random(seed).sample(...)` / `.choice(...)` — i.e. the exact
  assertions the old `test_random_pick`/`test_random_bundle` made, now
  against the new node.

### 5. Docs

- Update `web/docs/UtilityNodesTagsRandomPick.md` and
  `UtilityNodesTagsRandomBundle.md` for the new `spec` output socket.
- Add `web/docs/UtilityNodesTagsRandomBuild.md`.

### 6. Integration workflows (`tests/integration/workflows.json`)

Both `TagsRandomPick` and `TagsRandomBundle` cases currently wire their
`bundle` output straight into `TagsMerge`/the next node. Insert a
`UtilityNodesTagsRandomBuild` node between them and update the downstream
`inputs` reference (`["<random_node_id>", 0]` → `["<build_node_id>", 0]`).
Same expected final values (seed=7 sample, seed=0/5 choice) since resolution
logic is unchanged, just relocated.

## Verification

- `make check` (lint + typecheck + unit tests).
- `make integration` to confirm the rewired workflows still produce the same
  reference outputs end-to-end through real ComfyUI.

## Update — superseded by folding into TagsMerge

After implementing the above, scope was extended: instead of a standalone
`TagsRandomBuild` node, its resolution logic (`resolve_random_spec`) was
moved into `nodes/tags/_base.py` and `TagsMerge` itself gained `spec_1..10`
inputs. `TagsMerge` is now the pipeline's single terminal "build" step —
resolving specs (spec inputs first, then bundles, so explicit bundle
overrides win the usual last-occurrence MUTEX_GROUPS rule) before running
conflict resolution. `TagsRandomBuild` was deleted.
