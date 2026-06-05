---
name: danbooru-tag-node
description: Build or extend a ComfyUI tag-group node in this repo by extracting tags from a Danbooru wiki page or tag-search URL. Use when the user points at a Danbooru wiki page (e.g. https://danbooru.donmai.us/wiki_pages/X) or tag-search URL and asks to make/extend a prompt-builder node from it.
---

# Danbooru → tag-group node

This repo provides ComfyUI prompt-builder nodes whose only variable input is a list of Danbooru tags presented as individual BOOLEAN toggles. The recurring task: given a Danbooru wiki/tag-search URL, produce a curated tag list and wire it into a new or existing tag-group node.

## Repo conventions (must follow)

- Directory layout:
  - `nodes/tags/_base.py` — shared `TagNodeBase`
  - `nodes/tags/composition.py`, `nodes/tags/bad.py` — themes that don't belong to body/clothing
  - `nodes/tags/body/{hair,hands,feet,breasts,type,exposure,marks}.py` — anatomy themes
  - `nodes/tags/clothing/{state,outfit,underwear_swimwear,material,legwear_footwear,headwear_eyewear,accessory}.py` — clothing themes
  - `nodes/text/` — non-tag utilities (prompt_combinator, random_text_picker, list_shuffle, text_concat, pony_prompt_builder)
  - Place new tag themes under the matching subdir; new utility nodes under `nodes/text/`.
- All tag-group nodes share `TagNodeBase` from `nodes/tags/_base.py`. Each node file does NOT duplicate the base — it imports via a TYPE_CHECKING shim (mypy sees a normal package import; runtime imports the spec-registered name):

  ```python
  from typing import TYPE_CHECKING

  if TYPE_CHECKING:
      from nodes.tags._base import TagNodeBase
  else:
      from _cuun_tag_node_base import TagNodeBase
  ```

  Then just `class FooBar(TagNodeBase): TAGS = _FOO`. For groups whose BOOLEAN default should be `True` (e.g. negative-prompt bad-tag families), override `DEFAULT_BOOLEAN: ClassVar[bool] = True` on the subclass.

- `TagNodeBase` provides: `RETURN_TYPES = ("STRING", TAGS_TYPE)` / `RETURN_NAMES = ("prompt", "bundle")`; `INPUT_TYPES` with `separator` + `preset` combo (`custom`/`all_on`/`all_off`/`invert`) + one BOOLEAN per tag (defaulting from `cls.DEFAULT_BOOLEAN`) + optional `extra`; and `build(self, separator, extra="", **kwargs)` that pops `preset` from kwargs and applies preset logic. The build return shape is `{"ui": {"text": (prompt,)}, "result": (prompt, bundle)}` where `bundle` is a `tuple[TaggedSelection, ...]` carrying the structured payload.
- **Every subclass MUST set `CATEGORY_ID: ClassVar[str]`, `LAYER: ClassVar[str]`, and `MUTEX_WITHIN: ClassVar[bool]`** above its `TAGS = _FOO` line. Patterns:
  - `CATEGORY_ID` — dotted path used by `TagsMerge` for mutex dedupe. Format `<layer>.<theme>[.<subgroup>]`, e.g. `body.hair.length_style`, `clothing.footwear`, `nsfw.position`.
  - `LAYER` — coarse bucket (`bad`, `composition`, `anatomy`, `exposure`, `clothing`, `nsfw_act`, `nsfw_state`). Used for cross-layer conflict resolution.
  - `MUTEX_WITHIN` — `True` for pick-one groups (hair length/color, body skin tone, position, footwear, etc.). `False` for additive groups (marks, accessories, gesture).
- If the new theme has tag-level conflicts with other themes (e.g. ``barefoot`` should suppress ``thighhighs``), edit ``nodes/tags/_conflicts.py``'s ``TAG_CONFLICTS`` map. Conflict resolution is **per-tag, not per-category** — listing precise tags is the convention. For broad sweeps, build the drop set from sibling tag tuples via ``from nodes.tags.clothing.X import _Y``.

- `__init__.py` MUST load `_tag_node_base.py` FIRST (registers `_cuun_tag_node_base` in `sys.modules`) before any tag-node file. Tests rely on `tests/conftest.py` doing the same pre-registration.
- Reference implementations (see the directory layout above):
  - `nodes/tags/bad.py` — 5 subclasses overriding `DEFAULT_BOOLEAN = True` (used as negative prompt)
  - `nodes/tags/composition.py`, `nodes/tags/body/*.py`, `nodes/tags/clothing/*.py` — default `False` (user picks one or a few positively)
- Pick the right default:
  - Default **True** when the whole group is sensibly thrown at the negative prompt (e.g. bad anatomy)
  - Default **False** when the user picks one or a few (angles, framing, focus)
- Single source file per theme. All subclasses extend the shared `TagNodeBase` (no per-file base anymore). Register all in `NODE_CLASS_MAPPINGS` / `NODE_DISPLAY_NAME_MAPPINGS` and load from the root `__init__.py`.
- Tags preserve declaration order in the output; user-visible widget order matches the tuple order, so group related tags together.
- Hyphenated tag names (`close-up`, `three-quarter_view`) are valid — they pass through `**kwargs`.

## Researching tags

Order of preference when locating tags:

1. The wiki page the user gave you — read its "see also", sub-tags, and example tag lists with WebFetch.
2. The Danbooru tag search page for prefix-style families:
   `https://danbooru.donmai.us/tags?commit=Search&search%5Bcategory%5D=0&search%5Bhide_empty%5D=yes&search%5Bname_or_alias_matches%5D=PREFIX_%2A&search%5Border%5D=count`
   - Walk pages 1, 2, 3 until results become irrelevant (character names, memes, costumes). Usually 2 pages is enough.
3. Companion wiki pages mentioned in "see also" of the primary page, to discover sibling tags (`bad_anatomy` → `anatomical_nonsense` → `artistic_error`).

## Curating

- Drop noise: character names, cosplay tags, memes, brand names, songs, copyright tags. They appear in count-ordered searches and are obvious from naming.
- Drop clothing/accessory tags when the user asked for "anatomy" / "body parts" / "パーツ系".
- Keep tags whose only failure mode is being niche — the user can untoggle. Skip only tags that are wrong-category or actively harmful.
- When a tag has plausible legitimate uses (e.g. `extra_ears` for catgirls), still include it but mention the caveat in the README note.
- **Color/pattern composites**: avoid pre-baked color+item tags (`black_thighhighs`, `white_shirt`, `striped_thighhighs`). Keep the base item (`thighhighs`, `shirt`) and let the user combine with a color via `extra` or `TextConcat`. Pattern words like `striped`/`polka_dot` belong in `nodes/tags/clothing/material.py` (Pattern subgroup), not duplicated per item.
- **Cross-file overlap**: nothing tests for it — check by grep when adding tags. Examples: `loose_necktie` lives in `clothing/state.py` so don't re-add it under `clothing/accessory.py` Neck; `mole_on_breast`/`breast_tattoo` live in `body/marks.py` so don't re-add under `body/breasts.py`.

## Decisions to surface (ask the user)

Before writing code, get explicit answers for:
1. **Scope** — which sub-family(ies) of tags from the page should be in this node? (e.g. wiki has body parts + objects + gender; user may want body parts only)
2. **Grouping** — one node or multiple? Use multiple when tag count exceeds ~20 or when sub-families are independently togglable (e.g. NSFW vs SFW). Mirror the existing 5-node split style.
3. **Default state** — True (negative-prompt batch) or False (positive-prompt pick-one)?
4. **Extending vs new** — if a similar node exists, prefer extending its tag list over creating a parallel node.

## Implementation checklist

For a new tag group:

1. Choose the target file under the matching subdir (`nodes/tags/body/<theme>.py` or `nodes/tags/clothing/<theme>.py`, or `nodes/tags/<theme>.py` if neither fits). Extend an existing file if it's the same theme.
2. Define the tag tuple(s) at module top in display order.
3. Add the TYPE_CHECKING shim for `TagNodeBase`, then `class FooBar(TagNodeBase): TAGS = _MY_TUPLE`.
4. Add entries to that file's `NODE_CLASS_MAPPINGS` and `NODE_DISPLAY_NAME_MAPPINGS`.
5. If you created a new file, add a `_load(...)` entry in the root `__init__.py`.
6. **Do NOT write per-theme tests.** The core logic lives in `TagNodeBase` and is covered once by `tests/tags/test_base.py` (synthetic subclasses). New themes are just data (the `TAGS` tuple) — there is nothing per-theme worth asserting. Use `git diff` as the source of truth for tag-list changes, and trust no-overlap by reading the diff.
7. Update the README table for that theme.
8. Run `make check`. Fix lint/format/typecheck/test failures before reporting done.

## Don'ts

- Don't import across sibling theme files (e.g. `from nodes.tags.body.hair import ...` in another tag file) — each is loaded via `spec_from_file_location` with a private name and can't see other tag-node modules. Only `TagNodeBase` (loaded first into `sys.modules` as `_cuun_tag_node_base`) is shareable.
- Don't write a separate JS extension for preview — the existing `ui.text` return is enough.
- Don't forget to add the `_load(...)` line in the root `__init__.py` when introducing a new theme file. Tests will pass without it but the node won't appear in ComfyUI.
- Don't paste 50+ tags without checking page 2/3 of the Danbooru count-ordered search — comprehensive coverage is the whole point of this skill.
