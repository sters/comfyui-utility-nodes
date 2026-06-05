"""Cross-layer conflict rules for TagsMerge.

If a tag from `TAG_OVERRIDES` shows up anywhere in the merged bundle, every
selection whose `category` startswith any prefix in the override-set is
dropped. Layer-level prefixes (e.g. ``"clothing"``) match all sub-categories.

Edge cases (documented, not auto-handled):
- ``no_panties`` doesn't fire — partial-underwear suppression is too tightly
  bound to which underwear was selected. Curate by hand.
- ``topless`` drops ``clothing.tops`` and ``clothing.underwear`` since a bra
  is also a top-half item. If you want "topless under open jacket", manually
  un-toggle ``topless`` and use ``open_jacket`` instead.
"""

NODE_CLASS_MAPPINGS: dict[str, type] = {}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {}

TAG_OVERRIDES: dict[str, frozenset[str]] = {
    "nude": frozenset({"clothing"}),
    "completely_nude": frozenset({"clothing"}),
    "topless": frozenset({"clothing.tops", "clothing.underwear"}),
    "bottomless": frozenset({"clothing.bottoms"}),
    "barefoot": frozenset({"clothing.footwear"}),
    "no_shoes": frozenset({"clothing.footwear"}),
    "no_legwear": frozenset({"clothing.legwear"}),
}


def category_matches(category: str, prefixes: frozenset[str]) -> bool:
    """True iff `category` equals or is a dotted descendant of any prefix."""
    return any(category == p or category.startswith(p + ".") for p in prefixes)
