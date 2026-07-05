from nodes.tags._base import Spec, TaggedSelection
from nodes.tags.inspector import TagsBundleInspector


def _sel(layer: str, category: str, tags: tuple[str, ...]) -> TaggedSelection:
    return TaggedSelection(category=category, layer=layer, tags=tags)


def _fixed(*sels: TaggedSelection) -> Spec:
    return Spec(kind="fixed", pool=sels)


def test_passthrough_bundle_identity() -> None:
    bundle = _fixed(_sel("base", "hair_color", ("red_hair",)))
    out = TagsBundleInspector().inspect(bundle)
    assert out[0] == bundle


def test_report_groups_by_layer() -> None:
    bundle = _fixed(
        _sel("base", "hair_color", ("red_hair",)),
        _sel("base", "eye_color", ("blue_eyes",)),
        _sel("clothing", "outfit", ("school_uniform",)),
    )
    report = TagsBundleInspector().inspect(bundle)[1]
    assert "[base]" in report
    assert "[clothing]" in report
    assert "red_hair" in report
    assert "school_uniform" in report
    # Layer order follows first-seen order in the bundle.
    assert report.index("[base]") < report.index("[clothing]")


def test_report_appends_warnings_when_present() -> None:
    bundle = _fixed(_sel("base", "hair_color", ("red_hair",)))
    warnings = "mutex_group: kept 'red_hair', dropped ['brown_hair']"
    report = TagsBundleInspector().inspect(bundle, warnings=warnings)[1]
    assert "--- dropped ---" in report
    assert "brown_hair" in report


def test_report_omits_dropped_section_when_no_warnings() -> None:
    bundle = _fixed(_sel("base", "hair_color", ("red_hair",)))
    report = TagsBundleInspector().inspect(bundle, warnings="   ")[1]
    assert "--- dropped ---" not in report


def test_empty_bundle_renders_placeholder() -> None:
    report = TagsBundleInspector().inspect(Spec(kind="fixed", pool=()))[1]
    assert "empty bundle" in report
