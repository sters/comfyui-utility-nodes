from nodes.tags.sources.preset._base import RANDOM_OPTION
from nodes.tags.sources.preset.act import ACT_PRESETS, ActPreset


def test_input_types_lists_all_acts() -> None:
    spec = ActPreset.INPUT_TYPES()
    options, meta = spec["required"]["act"]
    assert set(options) == set(ACT_PRESETS) | {RANDOM_OPTION}
    assert meta["default"] == RANDOM_OPTION


def test_selfie_peace_emits_expected_tags() -> None:
    bundle = ActPreset().build("selfie_peace")[0]
    tags = bundle.pool[0].tags
    for expected in ("selfie", "holding_phone", "peace_sign", "smile"):
        assert expected in tags


def test_all_act_tags_exist_in_some_tag_node() -> None:
    """Every tag in every SFW act preset should be registered in one of
    the tag nodes — otherwise it's a typo or invented tag."""
    from tests.tags.test_build import _TAG_INDEX

    unknown: dict[str, list[str]] = {}
    for name, tags in ACT_PRESETS.items():
        for t in tags:
            if t not in _TAG_INDEX:
                unknown.setdefault(name, []).append(t)
    assert not unknown, f"unknown tags: {unknown}"
