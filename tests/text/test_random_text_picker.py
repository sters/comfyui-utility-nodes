from nodes.text.random_text_picker import RandomTextPicker


def test_pick_basic() -> None:
    node = RandomTextPicker()
    (out,) = node.pick("a,b,c,d,e", ",", 3, seed=42)
    parts = out.split(",")
    assert len(parts) == 3
    assert len(set(parts)) == 3
    for p in parts:
        assert p in {"a", "b", "c", "d", "e"}


def test_pick_is_deterministic_with_seed() -> None:
    node = RandomTextPicker()
    (a,) = node.pick("a,b,c,d,e", ",", 3, seed=123)
    (b,) = node.pick("a,b,c,d,e", ",", 3, seed=123)
    assert a == b


def test_pick_different_seeds_differ() -> None:
    node = RandomTextPicker()
    results = {node.pick("a,b,c,d,e,f,g,h", ",", 4, seed=s)[0] for s in range(20)}
    assert len(results) > 1


def test_count_larger_than_items_returns_all() -> None:
    node = RandomTextPicker()
    (out,) = node.pick("a,b,c", ",", 10, seed=1)
    assert sorted(out.split(",")) == ["a", "b", "c"]


def test_empty_text_returns_empty() -> None:
    node = RandomTextPicker()
    (out,) = node.pick("", ",", 3, seed=1)
    assert out == ""


def test_strips_whitespace_and_drops_empty() -> None:
    node = RandomTextPicker()
    (out,) = node.pick("a, b , ,c,", ",", 3, seed=1)
    parts = out.split(",")
    assert sorted(parts) == ["a", "b", "c"]


def test_escape_sequence_delimiter() -> None:
    node = RandomTextPicker()
    (out,) = node.pick("a\nb\nc", "\\n", 2, seed=1)
    parts = out.split("\n")
    assert len(parts) == 2
    for p in parts:
        assert p in {"a", "b", "c"}
