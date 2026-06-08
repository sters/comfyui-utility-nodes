"""Issue #13: negative-prompt quality nodes.

`bad.py` provides five negative-quality tag nodes (general / head & face /
body / limbs / NSFW) so the negative prompt has the same toggle-driven UX as
the positive side. They default all-on because a negative prompt usually wants
the full anti-artefact set; turn off the few you don't want.
"""

import pytest

from nodes.tags._base import TagNodeBase
from nodes.tags.sources.meta.bad import (
    BadBody,
    BadGeneral,
    BadHeadFace,
    BadLimbs,
    BadNSFW,
)

_NODES: list[tuple[type[TagNodeBase], str, str]] = [
    (BadGeneral, "bad.general", "bad_anatomy"),
    (BadHeadFace, "bad.head_face", "bad_face"),
    (BadBody, "bad.body", "bad_torso"),
    (BadLimbs, "bad.limbs", "bad_hands"),
    (BadNSFW, "bad.nsfw", "bad_vulva"),
]


@pytest.mark.parametrize("cls,category_id,sample_tag", _NODES)
def test_bad_nodes_default_all_on(cls: type[TagNodeBase], category_id: str, sample_tag: str) -> None:
    spec = cls.INPUT_TYPES()
    for tag in cls.TAGS:
        assert spec["required"][tag][1]["default"] is True, f"{tag} should default on"
    assert sample_tag in cls.TAGS
    assert category_id == cls.CATEGORY_ID
    assert cls.LAYER == "bad"


@pytest.mark.parametrize("cls,category_id,sample_tag", _NODES)
def test_bad_node_emits_bundle(cls: type[TagNodeBase], category_id: str, sample_tag: str) -> None:
    node = cls()
    tags = dict.fromkeys(cls.TAGS, False)
    tags[sample_tag] = True
    (bundle,) = node.build(", ", "", **tags)["result"]
    assert bundle[0].category == category_id
    assert bundle[0].tags == (sample_tag,)
