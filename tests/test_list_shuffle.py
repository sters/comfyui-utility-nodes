from nodes.list_shuffle import ListShuffle


def test_shuffle_deterministic() -> None:
    node = ListShuffle()
    (a,) = node.shuffle(["a", "b", "c", "d", "e"], [42], [0])
    (b,) = node.shuffle(["a", "b", "c", "d", "e"], [42], [0])
    assert a == b
    assert sorted(a) == ["a", "b", "c", "d", "e"]


def test_shuffle_changes_order() -> None:
    node = ListShuffle()
    src = [str(i) for i in range(20)]
    (out,) = node.shuffle(src, [1], [0])
    assert out != src
    assert sorted(out) == sorted(src)


def test_limit_caps_length() -> None:
    node = ListShuffle()
    (out,) = node.shuffle(["a", "b", "c", "d", "e"], [7], [3])
    assert len(out) == 3
    for item in out:
        assert item in {"a", "b", "c", "d", "e"}


def test_limit_zero_returns_all() -> None:
    node = ListShuffle()
    (out,) = node.shuffle(["a", "b", "c"], [0], [0])
    assert sorted(out) == ["a", "b", "c"]


def test_limit_larger_than_items_returns_all() -> None:
    node = ListShuffle()
    (out,) = node.shuffle(["a", "b", "c"], [0], [99])
    assert sorted(out) == ["a", "b", "c"]


def test_empty_input() -> None:
    node = ListShuffle()
    (out,) = node.shuffle([], [0], [0])
    assert out == []
