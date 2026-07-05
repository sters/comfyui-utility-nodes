# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Dependencies are managed by `uv`. All commands go through the Makefile:

- `make sync` — install dependencies
- `make test` — run pytest (`uv run pytest`)
- `make lint` / `make fmt` / `make fmt-check` / `make typecheck` — ruff + mypy (strict)
- `make check` — lint + fmt-check + typecheck + test (run before committing)
- `make fix` — ruff `--fix` + format
- Run a single test: `uv run pytest tests/tags/test_build.py::test_name -v`
- `make integration` — end-to-end check. Builds a CPU-only ComfyUI Docker image, starts it with this repo mounted as a custom node, posts workflows to `/prompt`, asserts text outputs from `/history`, tears down. Stdlib-only runner. See `tests/integration/README.md`. Intentionally not part of `make check` (first-build Docker cost).

**Both are cheap to run — don't hesitate to run them.** `make check` is a sub-second offline suite (~360 pytest cases plus ruff/mypy). `make integration` only pays the Docker build once (cached after, ~1.5 GB); every run after that is just container-up → ~25 HTTP workflow checks → teardown, a handful of seconds. If you only changed an integration `workflows.json` expectation and the container is already up, you can skip the rebuild and re-run just the runner: `uv run python -m tests.integration.run`. Run them liberally to verify changes — especially `make integration` after touching any node I/O surface or `workflows.json`.

Target Python is 3.10, mypy is `strict = true`, ruff line length 120.

## Architecture

This is a ComfyUI custom-node pack. ComfyUI discovers nodes via `NODE_CLASS_MAPPINGS` / `NODE_DISPLAY_NAME_MAPPINGS` at the package root (`__init__.py`).

ComfyUI custom-node docs: https://docs.comfy.org/custom-nodes/walkthrough (and the wider `https://docs.comfy.org/custom-nodes/` section). Consult these when touching node I/O surfaces — `INPUT_TYPES`, `RETURN_TYPES`, `OUTPUT_NODE`, `OUTPUT_IS_LIST`, custom socket types like `CUUN_TAGS`, etc.

### Module loading and auto-discovery

`__init__.py` walks `nodes/` with `pkgutil.walk_packages`, imports each module, and merges any `NODE_CLASS_MAPPINGS` / `NODE_DISPLAY_NAME_MAPPINGS` it exposes. Files whose basename starts with `_` (e.g. `_base.py`, `_conflicts.py`) are skipped. **You do not need to register new nodes anywhere** — dropping a file under `nodes/.../foo.py` with the two mappings is enough.

### Layout

Two halves under `nodes/tags/`:

- `nodes/tags/` (top level) — **tag operations**: `build.py`, `decorate.py`, `explode.py`, `combinator.py`, plus the shared `_base.py` / `_conflicts.py`. These take CUUN_TAGS bundles and transform/combine them. The one outlier is `count_extract.py` (`TagsExtractSubjectCount`), which *consumes* a prompt STRING (typically `TagsBuild.prompt`) and extracts an INT person count — it still belongs here as a tag operation, not under `sources/`, because it does not emit a CUUN_TAGS bundle.
- `nodes/tags/sources/` — **tag sources** (every `TagNodeBase` subclass): the boolean-toggle nodes (`body/`, `clothing/`, `scene/`, `composition/`, `meta/` [including `bad.py` negative-quality and `pony.py` model template], `nsfw/`, `decoration/`) and the flat-tuple preset nodes under `preset/` (`character.py`, `personality.py`, `situation.py`, `nsfw_scene.py`).

Auto-discovery walks both via `pkgutil.walk_packages`, so dropping a file under either path is enough to register it.

### Node menu category (the `CATEGORY` field)

ComfyUI's Add-Node menu groups nodes by their `CATEGORY` string. The root is `UtilityNodes`, with `TagMaster` as the tag sub-pack: `UtilityNodes/TagMaster/Body`, `.../Clothing`, `.../Body/Face`, `.../Preset`, `.../Meta`, `.../NSFW`, etc.

`TagNodeBase` subclasses **don't set `CATEGORY` themselves** — `__init_subclass__` derives it from the module path via `category_for_module` in `_base.py` (`nodes.tags.sources.body.hair` → `UtilityNodes/TagMaster/Body`; the `tags.sources` prefix collapses to `TagMaster`, and `_SEGMENT_OVERRIDES` handles special-cased names like `nsfw` → `NSFW`). Non-`TagNodeBase` nodes (the tag operations, the preset/pony nodes, text/image nodes) spell out `CATEGORY` explicitly. Display names (`NODE_DISPLAY_NAME_MAPPINGS`) drop any folder prefix the category already conveys and carry no default/behavior parentheticals — e.g. `Body: Figure` → `Figure`, but `Hair: Color` keeps its prefix because hair shares the `Body` folder.

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

The bulk of the repo is "tag nodes" — boolean-checkbox UIs that emit tag tuples. Data flows:

```
TagNodeBase subclass  ──►  bundle: tuple[TaggedSelection, ...]  ──►  TagsBuild  ──►  prompt
                                  (CUUN_TAGS socket)
```

Key types in `nodes/tags/_base.py`:

- `TaggedSelection(category, layer, tags, mutex_within)` — one categorized chunk.
- `TagNodeBase` — base class. Subclasses declare `TAGS`, `CATEGORY_ID`, `LAYER`, `MUTEX_WITHIN`. The base auto-builds the boolean `INPUT_TYPES`, exposes an `invert` BOOLEAN that flips every checkbox, and emits one `TaggedSelection` (plus an optional `extra` selection for free-form text). The only output socket is `bundle` (a tuple of `TaggedSelection`) — wire it through `TagsBuild` (or `TagsCombinator`) when you need a STRING. Every node in this pack is a **pure data node**: `build`/`merge`/etc. return their result tuple directly, and **none set `OUTPUT_NODE`** (there is no in-canvas text preview — that was dropped because rendering `ui.text` needs a frontend JS widget the pack doesn't ship). A graph of only these nodes therefore needs a real terminator (a sampler, or a built-in `PreviewAny`) to execute.

`TagsBuild` (`nodes/tags/build.py`) accepts up to 10 `CUUN_TAGS` inputs and applies, in order:

1. **`mutex_within`** — for selections marked mutex, keep only the first selection per `category` and only its first tag.
2. **`MUTEX_GROUPS`** (in `_conflicts.py`) — cross-category sets where at most one member survives (e.g. `long_hair` vs `short_hair`). First occurrence in input order wins.
3. **`TAG_CONFLICTS`** — per-tag suppression map: presence of a trigger drops a set of suppressed tags from every non-`extra` selection. Triggers themselves are never dropped.
4. Flatten surviving tags in input order, append `extra`, join with `separator`. Returns `(prompt, warnings, bundle)`.

`nodes/tags/_conflicts.py` is the **single source of truth for cross-node conflicts**. It pulls subsets (e.g. `_BRAS`, `_PANTIES`, `_LEGWEAR`) from `sources/clothing/` modules and composes them into `MUTEX_GROUPS` and `TAG_CONFLICTS`. When adding a tag that interacts with others across nodes (e.g. a new bottoms tag vs. `bottomless`), wire it through `_conflicts.py` rather than the node module — the merge step is where conflict semantics live.

Preset nodes live under `nodes/tags/sources/preset/` (`character.py`, `personality.py`, `situation.py`, `nsfw_scene.py`) and emit a flat tuple of pre-composed tags as one or more `TaggedSelection`s; the same merge pipeline still resolves layering with regular tag nodes.

### Text nodes

`nodes/text/` contains plain prompt utilities (`ListShuffle`, `TextConcat`, `RandomTextPicker`). They are independent of the tag-node bundle system. Combinatorial expansion happens on the tag side via `TagsCombinator` (`nodes/tags/combinator.py`) — there is no STRING-axis combinator, because every axis worth varying in this pack is already a tag bundle.

### Test layout

`tests/` mirrors `nodes/` 1:1 for everything that carries **behavior** — tag operations (including `count_extract`), presets, the meta nodes (`count`/`bad`/`pony`/`quality`), text, image, and util. When a module under one of those areas has a test, it lives at the mirror path:

```
nodes/tags/X.py             ←→  tests/tags/test_X.py
nodes/tags/sources/sub/X.py ←→  tests/tags/sources/sub/test_X.py
nodes/text/X.py             ←→  tests/text/test_X.py
```

**Plain `TagNodeBase` toggle sources are intentionally not unit-tested.** The boolean-checkbox source modules (`body/`, `clothing/`, `scene/`, `composition/`, `nsfw/`, `decoration/`) are pure declarative `TAGS` tuples with zero per-node logic — the base class is what's tested (`tests/tags/test_base.py`), and the tags themselves are exercised end-to-end through `TagsBuild` / the preset-combo fixture. **Do not add a one-test-per-toggle-source file** to "complete" the mirror; that's churn with no coverage gain. Only add a test when a source has non-trivial behavior (e.g. `count_extract` parses a prompt) — and then it goes at the mirror path. If you split or move a *tested* module, move its test the same way.

`tests/tags/sources/preset/test_combos.py` is the one cross-cutting fixture: it exercises preset × preset × scene combinations through `TagsBuild` end-to-end and is the canonical place to add a regression when a conflict rule changes.

### Naming conventions

Four surfaces must stay in lockstep — folder path, file name, class name, and ComfyUI display name. Rules in force:

- **Class prefix follows the source folder.** Body sources are `Body*` (`BodyPosture`, `BodySeating` — note: not `Whole*`), clothing `Clothing*`, scene `Scene*`, composition `Composition*`, face `Face*` (with `FaceEyes*` / `FaceMouth*` sub-groups), nsfw `Nsfw*`. The `meta/` folder is the one folder hosting **two** prefixes by design: `Meta*` (`MetaQuality`, `MetaPony`, `MetaCount*`) for the template/quality/count nodes and `Bad*` (`BadBody`, `BadNsfw`, …) for the negative-quality "Bad: X" family — keep that split, don't unify them.
- **Tag *operations* (`nodes/tags/` top level) are `Tags*` plural** — `TagsBuild`, `TagsExplode`, `TagsDecorate`, `TagsFilter`, `TagsCombinator`, `TagsExtractSubjectCount`, etc. (No singular `Tag*`.)
- **No abbreviations in class names** — spell words out (`SceneBackgroundType`, not `SceneBgType`).
- **Acronyms are mixed-case in class names, UPPERCASE in display names** — class `BadNsfw` / `NsfwSolo`, display `"Bad: NSFW"` / category `NSFW`. Keep class-name acronym casing as `Nsfw` / `Bdsm` everywhere; the all-caps form only appears in the human-facing display string.
- **The registered key (`class_type`) is `UtilityNodes` + the class name** — every key in `NODE_CLASS_MAPPINGS` / `NODE_DISPLAY_NAME_MAPPINGS` carries the `UtilityNodes` prefix (`TagsBuild` → key `UtilityNodesTagsBuild`), so a same-named node from another pack can never shadow ours in ComfyUI's single global mapping (issue #25). The **Python class name stays unprefixed** (`TagsBuild`) and so does the **display name**; only the registration key gets the prefix. The **`web/docs/<class_type>.md` filename equals the prefixed key** (`UtilityNodesTagsBuild.md`), because ComfyUI resolves help pages by `class_type`. Renaming a class means renaming its doc file (prefixed), both mapping keys (prefixed), any `class_type` in `tests/integration/workflows.json`, the `type` / `Node name for S&R` in `example_workflows/*.json`, and the test references. `__init__.py` also registers an `old_id -> new_id` ComfyUI **node replacement** for every node (bare name → prefixed) so legacy saved workflows auto-upgrade on load; that registration is derived automatically from the prefix, no per-node step.
- **Display names drop the folder prefix the category already conveys** (`BodyAction` → `Action`) but **keep an in-folder sub-group prefix with a colon** (`HairColor` → `Hair: Color`, `FaceEyesColor` → `Eyes: Color`), and carry no default/behavior parentheticals.

## Adding a new tag node

1. Create `nodes/tags/sources/.../foo.py` with a `TagNodeBase` subclass and a module-level `NODE_CLASS_MAPPINGS` / `NODE_DISPLAY_NAME_MAPPINGS`. **Keys must be `UtilityNodes`-prefixed** (`{"UtilityNodesFoo": Foo}`, `{"UtilityNodesFoo": "Foo"}`); the class name and display name stay unprefixed. Use relative imports — `from ..._base import TagNodeBase` for files at `sources/<subpkg>/foo.py`, `from .._base import ...` for files directly under `sources/`.
2. Auto-discovery picks it up — no registration step.
3. If the new tags conflict with existing ones, edit `_conflicts.py` — not the node file.
4. A plain toggle source (just a `TAGS` tuple, no logic) needs **no test** — see "Test layout". Add a test only if the node has real behavior, at the mirror path (`tests/tags/sources/.../test_foo.py`, or `tests/tags/test_foo.py` for an operation).
5. Add an English help page at `web/docs/UtilityNodes<ClassName>.md` ([Help Page](https://docs.comfy.org/custom-nodes/help_page)). `__init__.py` already exposes `WEB_DIRECTORY = "./web"`. Filename must match the registered `class_type` (i.e. the `UtilityNodes`-prefixed key). For ordinary tag nodes the existing files are mechanically generated from `TAGS` — keep that shape unless the node has non-trivial behavior to explain.

## Workflow templates

End-to-end ComfyUI workflows live under `example_workflows/` and are surfaced via ComfyUI's [Workflow Templates](https://docs.comfy.org/custom-nodes/workflow_templates) (Workflow → Browse Templates → `comfyui-utility-nodes`). JSON shape follows the [v1 workflow spec](https://docs.comfy.org/specs/workflow_json) — links are objects (`{id, origin_id, origin_slot, target_id, target_slot, type}`), not the legacy positional tuples. When adding a template, mirror its text portion as an API-format case in `tests/integration/workflows.json` so `make integration` catches regressions to the wiring.
