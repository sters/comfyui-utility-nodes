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

Target Python is 3.10, mypy is `strict = true`, ruff line length 120.

## Architecture

This is a ComfyUI custom-node pack. ComfyUI discovers nodes via `NODE_CLASS_MAPPINGS` / `NODE_DISPLAY_NAME_MAPPINGS` at the package root (`__init__.py`).

ComfyUI custom-node docs: https://docs.comfy.org/custom-nodes/walkthrough (and the wider `https://docs.comfy.org/custom-nodes/` section). Consult these when touching node I/O surfaces — `INPUT_TYPES`, `RETURN_TYPES`, `OUTPUT_NODE`, `OUTPUT_IS_LIST`, custom socket types like `CUUN_TAGS`, etc.

### Module loading and auto-discovery

`__init__.py` walks `nodes/` with `pkgutil.walk_packages`, imports each module, and merges any `NODE_CLASS_MAPPINGS` / `NODE_DISPLAY_NAME_MAPPINGS` it exposes. Files whose basename starts with `_` (e.g. `_base.py`, `_conflicts.py`) are skipped. **You do not need to register new nodes anywhere** — dropping a file under `nodes/.../foo.py` with the two mappings is enough.

Within node modules, use ordinary relative imports:

```python
from ._base import TagNodeBase           # sibling
from .._base import TAGS_TYPE            # parent
from .._conflicts import MUTEX_GROUPS
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
- `TagNodeBase` — base class. Subclasses declare `TAGS`, `CATEGORY_ID`, `LAYER`, `MUTEX_WITHIN`. The base auto-builds the boolean `INPUT_TYPES`, handles the `custom / all_on / all_off / invert` preset selector, and emits one `TaggedSelection` (plus an optional `extra` selection for free-form text). Outputs are `(prompt, bundle)` where `bundle` is a tuple of `TaggedSelection`.

`TagsMerge` (`nodes/tags/merge.py`) accepts up to 10 `CUUN_TAGS` inputs and applies, in order:

1. **`mutex_within`** — for selections marked mutex, keep only the first selection per `category` and only its first tag.
2. **`MUTEX_GROUPS`** (in `_conflicts.py`) — cross-category sets where at most one member survives (e.g. `long_hair` vs `short_hair`). First occurrence in input order wins.
3. **`TAG_CONFLICTS`** — per-tag suppression map: presence of a trigger drops a set of suppressed tags from every non-`extra` selection. Triggers themselves are never dropped.
4. Flatten surviving tags in input order, append `extra`, join with `separator`. Returns `(prompt, warnings, bundle)`.

`nodes/tags/_conflicts.py` is the **single source of truth for cross-node conflicts**. It pulls subsets (e.g. `_BRAS`, `_PANTIES`, `_LEGWEAR`) from clothing modules and composes them into `MUTEX_GROUPS` and `TAG_CONFLICTS`. When adding a tag that interacts with others across nodes (e.g. a new bottoms tag vs. `bottomless`), wire it through `_conflicts.py` rather than the node module — the merge step is where conflict semantics live.

Preset nodes (`preset.py`, `personality.py`, `nsfw_preset.py`) emit a flat tuple of pre-composed tags as one or more `TaggedSelection`s; the same merge pipeline still resolves layering with regular tag nodes.

### Text nodes

`nodes/text/` contains plain prompt utilities (`PromptCombinator`, `ListShuffle`, `TextConcat`, `PonyPromptBuilder`, `RandomTextPicker`). They are independent of the tag-node bundle system.

### Test layout

`tests/tags/test_preset_combos.py` exercises preset × preset × scene combinations through `TagsMerge` end-to-end — the canonical place to add a regression when a conflict rule changes. Per-module tests live alongside (`test_preset.py`, `test_personality.py`, `test_merge.py`, etc.).

## Adding a new tag node

1. Create `nodes/tags/.../foo.py` with a `TagNodeBase` subclass and a module-level `NODE_CLASS_MAPPINGS` / `NODE_DISPLAY_NAME_MAPPINGS`. Use relative imports (`from .._base import TagNodeBase`).
2. Auto-discovery picks it up — no registration step.
3. If the new tags conflict with existing ones, edit `_conflicts.py` — not the node file.
4. Add tests under `tests/tags/`.
