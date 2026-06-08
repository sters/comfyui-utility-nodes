# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Dependencies are managed by `uv`. All commands go through the Makefile:

- `make sync` — install dependencies
- `make test` — run pytest (`uv run pytest`)
- `make lint` / `make fmt` / `make fmt-check` / `make typecheck` — ruff + mypy (strict)
- `make check` — lint + fmt-check + typecheck + test (run before committing)
- `make fix` — ruff `--fix` + format
- Run a single test: `uv run pytest tests/tags/test_merge.py::test_name -v`
- `make integration` — end-to-end check. Builds a CPU-only ComfyUI Docker image, starts it with this repo mounted as a custom node, posts workflows to `/prompt`, asserts text outputs from `/history`, tears down. Stdlib-only runner. See `tests/integration/README.md`. Intentionally not part of `make check` (Docker build cost).

Target Python is 3.10, mypy is `strict = true`, ruff line length 120.

## Architecture

This is a ComfyUI custom-node pack. ComfyUI discovers nodes via `NODE_CLASS_MAPPINGS` / `NODE_DISPLAY_NAME_MAPPINGS` at the package root (`__init__.py`).

ComfyUI custom-node docs: https://docs.comfy.org/custom-nodes/walkthrough (and the wider `https://docs.comfy.org/custom-nodes/` section). Consult these when touching node I/O surfaces — `INPUT_TYPES`, `RETURN_TYPES`, `OUTPUT_NODE`, `OUTPUT_IS_LIST`, custom socket types like `CUUN_TAGS`, etc.

### Module loading and auto-discovery

`__init__.py` walks `nodes/` with `pkgutil.walk_packages`, imports each module, and merges any `NODE_CLASS_MAPPINGS` / `NODE_DISPLAY_NAME_MAPPINGS` it exposes. Files whose basename starts with `_` (e.g. `_base.py`, `_conflicts.py`) are skipped. **You do not need to register new nodes anywhere** — dropping a file under `nodes/.../foo.py` with the two mappings is enough.

### Layout

Two halves under `nodes/tags/`:

- `nodes/tags/` (top level) — **tag operations**: `merge.py`, `decorate.py`, `explode.py`, `tags_combinator.py`, plus the shared `_base.py` / `_conflicts.py`. These take CUUN_TAGS bundles and transform/combine them.
- `nodes/tags/sources/` — **tag sources** (every `TagNodeBase` subclass): the boolean-toggle nodes (`body/`, `clothing/`, `scene/`, `composition/`, `meta/` [including `bad.py` negative-quality and `pony.py` model template], `nsfw/`, `decoration/`) and the flat-tuple preset nodes under `preset/` (`character.py`, `personality.py`, `situation.py`, `nsfw_scene.py`).

Auto-discovery walks both via `pkgutil.walk_packages`, so dropping a file under either path is enough to register it.

Within node modules, use ordinary relative imports. Depth varies — count carefully:

```python
# nodes/tags/sources/preset/character.py (depth 3)
from ..._base import TAGS_TYPE, TaggedSelection

# nodes/tags/sources/clothing/outfit.py (depth 3)
from ..._base import TagNodeBase

# nodes/tags/sources/body/face/eyes.py (depth 4)
from ...._base import TagNodeBase

# nodes/tags/_conflicts.py (top-level, reaches into sources)
from .sources.clothing.outfit import _BOTTOMS
```

The repo directory name (`comfyui-utility-nodes`) is invalid as a Python identifier due to the hyphen, but relative imports resolve via `__package__` and don't depend on the top-level name — ComfyUI loads the package via `spec_from_file_location`, which sets `__package__` correctly.

`__init__.py` guards the auto-discovery block with `if __package__:` so that pytest collecting the file as a bare module (which would otherwise blow up on relative imports) is a silent no-op.

### Tag-node pipeline (the core abstraction)

The bulk of the repo is "tag nodes" — boolean-checkbox UIs that emit Danbooru-style tag tuples. Data flows:

```
TagNodeBase subclass  ──►  bundle: tuple[TaggedSelection, ...]  ──►  TagsMerge  ──►  prompt
                                  (CUUN_TAGS socket)
```

Key types in `nodes/tags/_base.py`:

- `TaggedSelection(category, layer, tags, mutex_within)` — one categorized chunk.
- `TagNodeBase` — base class. Subclasses declare `TAGS`, `CATEGORY_ID`, `LAYER`, `MUTEX_WITHIN`. The base auto-builds the boolean `INPUT_TYPES`, exposes an `invert` BOOLEAN that flips every checkbox, and emits one `TaggedSelection` (plus an optional `extra` selection for free-form text). The only output socket is `bundle` (a tuple of `TaggedSelection`); the flattened text still surfaces as the OUTPUT_NODE preview but isn't a separate output — wire `bundle` through `TagsMerge` (or `TagsCombinator`) when you need a STRING.

`TagsMerge` (`nodes/tags/merge.py`) accepts up to 10 `CUUN_TAGS` inputs and applies, in order:

1. **`mutex_within`** — for selections marked mutex, keep only the first selection per `category` and only its first tag.
2. **`MUTEX_GROUPS`** (in `_conflicts.py`) — cross-category sets where at most one member survives (e.g. `long_hair` vs `short_hair`). First occurrence in input order wins.
3. **`TAG_CONFLICTS`** — per-tag suppression map: presence of a trigger drops a set of suppressed tags from every non-`extra` selection. Triggers themselves are never dropped.
4. Flatten surviving tags in input order, append `extra`, join with `separator`. Returns `(prompt, warnings, bundle)`.

`nodes/tags/_conflicts.py` is the **single source of truth for cross-node conflicts**. It pulls subsets (e.g. `_BRAS`, `_PANTIES`, `_LEGWEAR`) from `sources/clothing/` modules and composes them into `MUTEX_GROUPS` and `TAG_CONFLICTS`. When adding a tag that interacts with others across nodes (e.g. a new bottoms tag vs. `bottomless`), wire it through `_conflicts.py` rather than the node module — the merge step is where conflict semantics live.

Preset nodes live under `nodes/tags/sources/preset/` (`character.py`, `personality.py`, `situation.py`, `nsfw_scene.py`) and emit a flat tuple of pre-composed tags as one or more `TaggedSelection`s; the same merge pipeline still resolves layering with regular tag nodes.

### Text nodes

`nodes/text/` contains plain prompt utilities (`ListShuffle`, `TextConcat`, `RandomTextPicker`). They are independent of the tag-node bundle system. Combinatorial expansion happens on the tag side via `TagsCombinator` (`nodes/tags/tags_combinator.py`) — there is no STRING-axis combinator, because every axis worth varying in this pack is already a tag bundle.

### Test layout

`tests/` mirrors `nodes/` 1:1 — every node module has exactly one test file, and they live at the corresponding path:

```
nodes/tags/X.py             ←→  tests/tags/test_X.py
nodes/tags/sources/X.py     ←→  tests/tags/sources/test_X.py
nodes/tags/sources/sub/X.py ←→  tests/tags/sources/sub/test_X.py
nodes/text/X.py             ←→  tests/text/test_X.py
```

**Keep this invariant when adding nodes or moving things around.** If you split a source file, split its test file the same way; if you move a source into a subpackage, move its test there too. The auto-discovery system is forgiving — pytest will find tests anywhere — but the 1:1 path mapping is what lets a reader jump from a node to its tests (and vice versa) without grepping.

`tests/tags/sources/test_preset_combos.py` is the one cross-cutting fixture: it exercises preset × preset × scene combinations through `TagsMerge` end-to-end and is the canonical place to add a regression when a conflict rule changes.

## Adding a new tag node

1. Create `nodes/tags/sources/.../foo.py` with a `TagNodeBase` subclass and a module-level `NODE_CLASS_MAPPINGS` / `NODE_DISPLAY_NAME_MAPPINGS`. Use relative imports — `from ..._base import TagNodeBase` for files at `sources/<subpkg>/foo.py`, `from .._base import ...` for files directly under `sources/`.
2. Auto-discovery picks it up — no registration step.
3. If the new tags conflict with existing ones, edit `_conflicts.py` — not the node file.
4. Add tests at the mirror path — `tests/tags/sources/.../test_foo.py` for a `nodes/tags/sources/.../foo.py` source, or `tests/tags/test_foo.py` for a `nodes/tags/foo.py` operation. One source/op file = one test file.
5. Add an English help page at `web/docs/<ClassName>.md` ([Help Page](https://docs.comfy.org/custom-nodes/help_page)). `__init__.py` already exposes `WEB_DIRECTORY = "./web"`. Filename must match the registered class name. For ordinary tag nodes the existing files are mechanically generated from `TAGS` — keep that shape unless the node has non-trivial behavior to explain.

## Workflow templates

End-to-end ComfyUI workflows live under `example_workflows/` and are surfaced via ComfyUI's [Workflow Templates](https://docs.comfy.org/custom-nodes/workflow_templates) (Workflow → Browse Templates → `comfyui-utility-nodes`). JSON shape follows the [v1 workflow spec](https://docs.comfy.org/specs/workflow_json) — links are objects (`{id, origin_id, origin_slot, target_id, target_slot, type}`), not the legacy positional tuples. When adding a template, mirror its text portion as an API-format case in `tests/integration/workflows.json` so `make integration` catches regressions to the wiring.
