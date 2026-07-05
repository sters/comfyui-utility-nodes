from nodes.tags._base import Spec
from nodes.tags.merge import TagsMerge
from nodes.tags.sources.preset.character import CharacterPreset
from nodes.tags.sources.preset.situation import SITUATION_PRESETS, SituationPreset


def _build_situation(name: str) -> Spec:
    return SituationPreset().build(name)[0]


def test_situation_preset_input_lists_all() -> None:
    spec = SituationPreset.INPUT_TYPES()
    options, meta = spec["required"]["situation"]
    assert set(options) == set(SITUATION_PRESETS)
    assert meta["default"] in SITUATION_PRESETS


def test_summer_beach_emits_expected_tags() -> None:
    bundle = _build_situation("summer_beach")
    tags = bundle.pool[0].tags
    for expected in ("beach", "ocean", "swimsuit"):
        assert expected in tags


def test_character_plus_situation_layers_cleanly() -> None:
    miko = CharacterPreset().build("miko")[0]
    shrine = _build_situation("shrine_visit")
    out = TagsMerge().merge(", ", bundle_1=miko, bundle_2=shrine)
    tokens = str(out[0]).split(", ")
    for t in ("miko", "hakama", "shrine"):
        assert t in tokens


def test_situation_extra_appended() -> None:
    out = SituationPreset().build("park_picnic", extra="1girl")
    bundle = out[0].pool
    preview = ", ".join(t for sel in bundle for t in sel.tags)
    assert preview.endswith(", 1girl")
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
