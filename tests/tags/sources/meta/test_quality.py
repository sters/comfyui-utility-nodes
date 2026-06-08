from nodes.tags.sources.meta.quality import _QUALITY, MetaQuality


def test_quality_defaults_all_off() -> None:
    # Issue #15: realistic/photoreal tags must not be baked in by default —
    # anime-style prompts want a clean slate.
    spec = MetaQuality.INPUT_TYPES()
    for tag in _QUALITY:
        assert spec["required"][tag][1]["default"] is False, f"{tag} should default off"


def test_quality_emits_only_checked_tags() -> None:
    node = MetaQuality()
    tags = dict.fromkeys(_QUALITY, False)
    tags["masterpiece"] = True
    tags["best_quality"] = True
    (bundle,) = node.build("", **tags)
    assert bundle[0].tags == ("masterpiece", "best_quality")
    assert bundle[0].category == "meta.quality"


def test_quality_empty_when_nothing_checked() -> None:
    node = MetaQuality()
    tags = dict.fromkeys(_QUALITY, False)
    out = node.build("", **tags)
    assert out == ((),)


def test_quality_invert_selects_the_rest() -> None:
    node = MetaQuality()
    tags = dict.fromkeys(_QUALITY, False)
    tags["realistic"] = True
    (bundle,) = node.build("", invert=True, **tags)
    expected = tuple(t for t in _QUALITY if t != "realistic")
    assert bundle[0].tags == expected
