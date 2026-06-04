---
name: danbooru-tag-node
description: Build or extend a ComfyUI tag-group node in this repo by extracting tags from a Danbooru wiki page or tag-search URL. Use when the user points at a Danbooru wiki page (e.g. https://danbooru.donmai.us/wiki_pages/X) or tag-search URL and asks to make/extend a prompt-builder node from it.
---

# Danbooru → tag-group node

This repo provides ComfyUI prompt-builder nodes whose only variable input is a list of Danbooru tags presented as individual BOOLEAN toggles. The recurring task: given a Danbooru wiki/tag-search URL, produce a curated tag list and wire it into a new or existing tag-group node.

## Repo conventions (must follow)

- All tag-group nodes inherit a small base class with:
  - `RETURN_TYPES = ("STRING",)`, `RETURN_NAMES = ("prompt",)`, `FUNCTION = "build"`, `CATEGORY = "utility/text"`, `OUTPUT_NODE = True`
  - `INPUT_TYPES` exposes a `separator` STRING widget + one BOOLEAN per tag + optional multiline `extra`
  - `build` returns `{"ui": {"text": (prompt,)}, "result": (prompt,)}` for in-node preview
- Reference implementations:
  - `nodes/danbooru_bad_tags.py` — `_BadTagsBase` + 5 subclasses (default `True`, used as negative prompt)
  - `nodes/composition_tags.py` — `_CompositionBase` + 5 subclasses (default `False`, used positively)
- Pick the right default:
  - Default **True** when the whole group is sensibly thrown at the negative prompt (e.g. bad anatomy)
  - Default **False** when the user picks one or a few (angles, framing, focus)
- Single source file per theme. Multiple subclasses share one `_FooBase` in that file. Register all in `NODE_CLASS_MAPPINGS` / `NODE_DISPLAY_NAME_MAPPINGS` and load from the root `__init__.py`.
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

## Decisions to surface (ask the user)

Before writing code, get explicit answers for:
1. **Scope** — which sub-family(ies) of tags from the page should be in this node? (e.g. wiki has body parts + objects + gender; user may want body parts only)
2. **Grouping** — one node or multiple? Use multiple when tag count exceeds ~20 or when sub-families are independently togglable (e.g. NSFW vs SFW). Mirror the existing 5-node split style.
3. **Default state** — True (negative-prompt batch) or False (positive-prompt pick-one)?
4. **Extending vs new** — if a similar node exists, prefer extending its tag list over creating a parallel node.

## Implementation checklist

For a new tag group:

1. Choose the target file: extend an existing `*_tags.py` if it's the same theme, otherwise create `nodes/<theme>_tags.py`.
2. Define the tag tuple(s) at module top in display order.
3. Subclass the base class, set `TAGS = _MY_TUPLE`.
4. Add entries to that file's `NODE_CLASS_MAPPINGS` and `NODE_DISPLAY_NAME_MAPPINGS`.
5. If you created a new file, add a `_load(...)` entry in the root `__init__.py`.
6. Write tests in `tests/test_<theme>_tags.py` covering:
   - all-on order matches tuple order
   - all-off returns empty
   - default BOOLEAN value matches the group's convention
   - `OUTPUT_NODE is True`
   - extra appended after tags
   - a hyphenated tag name actually works as kwarg (if any are present)
   - no overlap with sibling groups (`test_no_overlap_between_groups`)
   - `test_total_tag_count` exact-count assertion (update when tags change)
7. Update the README table for that theme.
8. Run `make check`. Fix lint/format/typecheck/test failures before reporting done.

## Don'ts

- Don't import across `nodes/*.py` files — each is loaded via `spec_from_file_location` with a private name; duplicate the small base class within the file instead.
- Don't write a separate JS extension for preview — the existing `ui.text` return is enough.
- Don't forget to add the `_load(...)` line in the root `__init__.py` when introducing a new theme file. Tests will pass without it but the node won't appear in ComfyUI.
- Don't paste 50+ tags without checking page 2/3 of the Danbooru count-ordered search — comprehensive coverage is the whole point of this skill.
