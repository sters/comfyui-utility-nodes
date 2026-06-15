from nodes.image.metadata import (
    _to_str,
    annotated_output_path,
    first_path_line,
    format_metadata,
    get_metadata_value,
    parse_formatted_metadata,
    parse_metadata_text,
    stringify_info,
)


def test_parse_key_equals_value() -> None:
    assert parse_metadata_text("author=sters\nrating=5") == {"author": "sters", "rating": "5"}


def test_parse_key_colon_value() -> None:
    assert parse_metadata_text("author: sters\nnote: hi there") == {"author": "sters", "note": "hi there"}


def test_parse_equals_wins_over_colon_so_values_keep_colons() -> None:
    # A timestamp value contains colons — `=` must be the separator, not `:`.
    assert parse_metadata_text("created=2026-06-15T12:30:00") == {"created": "2026-06-15T12:30:00"}


def test_parse_json_object() -> None:
    assert parse_metadata_text('{"author": "sters", "seed": 42}') == {"author": "sters", "seed": "42"}


def test_parse_skips_blank_and_comment_and_separatorless_lines() -> None:
    text = "\n# a comment\nauthor=sters\n\nbare line with no separator\nrating=5\n"
    assert parse_metadata_text(text) == {"author": "sters", "rating": "5"}


def test_parse_empty_and_whitespace_is_empty_dict() -> None:
    assert parse_metadata_text("") == {}
    assert parse_metadata_text("   \n  \n") == {}


def test_parse_malformed_json_falls_back_to_lines() -> None:
    # Leading `{` triggers a JSON attempt; on failure we fall through to line
    # parsing, which finds no separator and yields nothing.
    assert parse_metadata_text("{not valid json") == {}


def test_parse_strips_surrounding_whitespace_on_key_and_value() -> None:
    assert parse_metadata_text("  author  =   sters  ") == {"author": "sters"}


def test_parse_later_duplicate_key_wins() -> None:
    assert parse_metadata_text("k=1\nk=2") == {"k": "2"}


def test_to_str_handles_bytes_tuple_int() -> None:
    assert _to_str(b"hello") == "hello"
    assert _to_str((72, 72)) == "(72, 72)"
    assert _to_str(42) == "42"
    assert _to_str("plain") == "plain"


def test_to_str_decodes_invalid_utf8_leniently() -> None:
    assert _to_str(b"\xff\xfe") == "��"


def test_stringify_info_coerces_keys_and_values() -> None:
    assert stringify_info({"dpi": (72, 72), 1: b"x"}) == {"dpi": "(72, 72)", "1": "x"}


def test_format_metadata_one_line_per_pair_in_order() -> None:
    assert format_metadata({"format": "PNG", "size": "512x512"}) == "format: PNG\nsize: 512x512"


def test_format_metadata_empty_is_empty_string() -> None:
    assert format_metadata({}) == ""


def test_parse_then_format_roundtrip_is_stable() -> None:
    pairs = parse_metadata_text("author=sters\nseed=42")
    assert format_metadata(pairs) == "author: sters\nseed: 42"


def test_annotated_output_path_without_subfolder() -> None:
    assert annotated_output_path("ComfyUI_meta_00001_.png", "") == "ComfyUI_meta_00001_.png [output]"


def test_annotated_output_path_with_subfolder() -> None:
    assert annotated_output_path("img_00001_.png", "batch_a") == "batch_a/img_00001_.png [output]"


def test_first_path_line_returns_first_nonblank() -> None:
    assert first_path_line("\n  a.png [output]\nb.png [output]\n") == "a.png [output]"


def test_first_path_line_empty_when_blank() -> None:
    assert first_path_line("") == ""
    assert first_path_line("   \n  ") == ""


def test_parse_formatted_metadata_roundtrips_format() -> None:
    dump = format_metadata({"author": "sters", "seed": "42"})
    assert parse_formatted_metadata(dump) == {"author": "sters", "seed": "42"}


def test_parse_formatted_metadata_keeps_colons_and_equals_in_value() -> None:
    # Splits on the first ": " only, so timestamps / formulae survive intact.
    dump = "created: 2026-06-15T12:30:00\nformula: a=b: c"
    assert parse_formatted_metadata(dump) == {"created": "2026-06-15T12:30:00", "formula": "a=b: c"}


def test_parse_formatted_metadata_skips_separatorless_lines() -> None:
    assert parse_formatted_metadata("no separator here\nk: v") == {"k": "v"}


def test_parse_formatted_metadata_empty_value() -> None:
    # format_metadata writes "key: " (trailing space) for an empty value.
    assert parse_formatted_metadata("note: ") == {"note": ""}


def test_get_metadata_value_found() -> None:
    dump = "author: sters\nseed: 42"
    assert get_metadata_value(dump, "seed") == ("42", True)


def test_get_metadata_value_missing_returns_default_and_false() -> None:
    assert get_metadata_value("author: sters", "seed", default="none") == ("none", False)


def test_get_metadata_value_missing_default_is_empty_string() -> None:
    assert get_metadata_value("author: sters", "seed") == ("", False)


def test_get_metadata_value_strips_key_whitespace() -> None:
    assert get_metadata_value("seed: 42", "  seed  ") == ("42", True)


def test_get_metadata_value_after_extract_header() -> None:
    # The dump ExtractImageMetadata produces — header then chunks — looks up fine.
    dump = "format: PNG\nsize: 64x64\nmode: RGB\nauthor: sters\nseed: 42"
    assert get_metadata_value(dump, "author") == ("sters", True)
    assert get_metadata_value(dump, "size") == ("64x64", True)
