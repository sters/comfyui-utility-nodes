from nodes.text.text_concat import TextConcat


def test_concat_basic() -> None:
    node = TextConcat()
    out = node.concat(", ", text_1="a", text_2="b", text_3="c")
    assert out[0] == "a, b, c"


def test_concat_preserves_order_with_gaps() -> None:
    node = TextConcat()
    out = node.concat(", ", text_1="a", text_3="c", text_5="e")
    assert out[0] == "a, c, e"


def test_concat_skips_none() -> None:
    node = TextConcat()
    out = node.concat(", ", text_1="a", text_2=None, text_3="c")
    assert out[0] == "a, c"


def test_concat_skips_empty_string() -> None:
    node = TextConcat()
    out = node.concat(", ", text_1="a", text_2="", text_3="c")
    assert out[0] == "a, c"


def test_concat_no_inputs() -> None:
    node = TextConcat()
    out = node.concat(", ")
    assert out[0] == ""


def test_concat_whitespace_value_kept() -> None:
    node = TextConcat()
    out = node.concat("|", text_1="a", text_2=" ", text_3="c")
    assert out[0] == "a| |c"


def test_concat_escape_separator() -> None:
    node = TextConcat()
    out = node.concat("\\n", text_1="a", text_2="b")
    assert out[0] == "a\nb"


def test_concat_empty_separator() -> None:
    node = TextConcat()
    out = node.concat("", text_1="a", text_2="b", text_3="c")
    assert out[0] == "abc"
