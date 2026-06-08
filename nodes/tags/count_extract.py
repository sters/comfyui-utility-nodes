import re
from typing import Any, ClassVar

# Pull Danbooru-style subject-count tags back out of an already-assembled
# prompt STRING (e.g. the output of TagsMerge). The motivating use case is
# feeding a person count into a downstream detector/segmenter such as SAM3
# (issue #19): wire TagsMerge.prompt -> this node -> `total` (INT).
#
# Recognised forms:
#   - numbered gendered:  1girl, 2girls, 3boys, 6+girls, 1other, 4others
#   - "multiple_*":       multiple_girls / multiple_boys / multiple_others
#   - total-only tags:    solo, solo_focus, duo, trio, couple, group
#
# `+` (as in `6+girls`) counts as the floor number (6). `multiple_*` with no
# explicit number contributes a floor of 2 for that gender. When no gendered
# tag is present, the total falls back to the solo/duo/trio/couple mapping;
# `group` alone leaves the total at 0 (count unknown — set it yourself).

_NUM_RE = re.compile(r"(?<![a-z0-9_])(\d+)\+?(girls?|boys?|others?)(?![a-z])")
_MULTI_RE = re.compile(r"(?<![a-z0-9_])multiple_(girl|boy|other)s(?![a-z])")
_TOTAL_RE = re.compile(r"(?<![a-z0-9_])(solo_focus|solo|duo|trio|couple|group)(?![a-z_])")

_TOTAL_MAP = {"solo": 1, "solo_focus": 1, "duo": 2, "trio": 3, "couple": 2, "group": 0}
_GENDERS = ("girl", "boy", "other")


class TagsExtractSubjectCount:
    """Extract subject-count tags and a person count from a prompt STRING."""

    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("STRING", "INT", "INT", "INT", "INT")
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("count_tags", "total", "girls", "boys", "others")
    FUNCTION: ClassVar[str] = "extract"
    CATEGORY: ClassVar[str] = "UtilityNodes/TagMaster"
    OUTPUT_NODE: ClassVar[bool] = True

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": ""}),
            },
        }

    def extract(self, prompt: str) -> dict[str, Any]:
        text = prompt.lower()
        counts = {g: 0 for g in _GENDERS}
        multi = {g: False for g in _GENDERS}
        tags: list[str] = []

        for m in _NUM_RE.finditer(text):
            n = int(m.group(1))
            gender = m.group(2).rstrip("s")
            counts[gender] = max(counts[gender], n)
            tag = m.group(0)
            if tag not in tags:
                tags.append(tag)

        for m in _MULTI_RE.finditer(text):
            gender = m.group(1)
            multi[gender] = True
            tag = m.group(0)
            if tag not in tags:
                tags.append(tag)

        total_tags = []
        for m in _TOTAL_RE.finditer(text):
            tag = m.group(1)
            if tag not in total_tags:
                total_tags.append(tag)

        # multiple_* with no explicit number -> floor of 2 for that gender.
        for g in _GENDERS:
            if counts[g] == 0 and multi[g]:
                counts[g] = 2

        total = counts["girl"] + counts["boy"] + counts["other"]
        if total == 0 and total_tags:
            total = max(_TOTAL_MAP.get(t, 0) for t in total_tags)

        ordered_tags = tags + total_tags
        count_tags = ", ".join(ordered_tags)
        preview = f"{total} subject(s): {count_tags}" if ordered_tags else "0 subject(s)"
        return {
            "ui": {"text": (preview,)},
            "result": (count_tags, total, counts["girl"], counts["boy"], counts["other"]),
        }


NODE_CLASS_MAPPINGS: dict[str, type] = {"TagsExtractSubjectCount": TagsExtractSubjectCount}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"TagsExtractSubjectCount": "Extract Subject Count"}
