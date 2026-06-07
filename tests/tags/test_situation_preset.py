from nodes.tags._base import TaggedSelection
from nodes.tags.merge import TagsMerge
from nodes.tags.sources.preset import CharacterPreset
from nodes.tags.sources.situation_preset import SITUATION_PRESETS, SituationPreset


def _build_situation(name: str) -> tuple[TaggedSelection, ...]:
    return tuple(SituationPreset().build(name, ", ")["result"][1])


def test_situation_preset_input_lists_all() -> None:
    spec = SituationPreset.INPUT_TYPES()
    options, meta = spec["required"]["situation"]
    assert set(options) == set(SITUATION_PRESETS)
    assert meta["default"] in SITUATION_PRESETS


def test_summer_beach_emits_expected_tags() -> None:
    bundle = _build_situation("summer_beach")
    tags = bundle[0].tags
    for expected in ("beach", "ocean", "swimsuit"):
        assert expected in tags


def test_character_plus_situation_layers_cleanly() -> None:
    miko = tuple(CharacterPreset().build("miko", ", ")["result"][1])
    shrine = _build_situation("shrine_visit")
    out = TagsMerge().merge(", ", bundle_1=miko, bundle_2=shrine)
    tokens = str(out["result"][0]).split(", ")
    for t in ("miko", "hakama", "shrine"):
        assert t in tokens


def test_situation_extra_appended() -> None:
    out = SituationPreset().build("park_picnic", ", ", extra="1girl")
    prompt = str(out["result"][0])
    assert prompt.endswith(", 1girl")
    bundle = tuple(out["result"][1])
    assert len(bundle) == 2
    assert bundle[1].category == "extra"


def test_all_situation_tags_exist_in_some_tag_node() -> None:
    """Every situation tag should be registered somewhere in the tag
    index — otherwise the model may not recognise it."""
    from tests.tags.test_merge import _TAG_INDEX

    unknown: dict[str, list[str]] = {}
    for name, tags in SITUATION_PRESETS.items():
        for t in tags:
            if t not in _TAG_INDEX:
                unknown.setdefault(name, []).append(t)
    assert not unknown, f"unknown tags: {unknown}"
