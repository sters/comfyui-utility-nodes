from nodes.util.seed import _MAX_SEED, SharedSeed


def test_seed_passthrough() -> None:
    out = SharedSeed().get(12345)
    assert out == (12345,)
    assert str(out[0]) == "12345"


def test_seed_coerced_to_int() -> None:
    out = SharedSeed().get(7.0)  # type: ignore[arg-type]
    assert out == (7,)
    assert isinstance(out[0], int)


def test_input_types_enables_control_after_generate() -> None:
    spec = SharedSeed.INPUT_TYPES()
    kind, meta = spec["required"]["seed"]
    assert kind == "INT"
    assert meta["control_after_generate"] is True
    assert meta["min"] == 0
    assert meta["max"] == _MAX_SEED


def test_output_contract() -> None:
    assert SharedSeed.RETURN_TYPES == ("INT",)
    assert SharedSeed.RETURN_NAMES == ("seed",)
    assert SharedSeed.CATEGORY == "UtilityNodes/Util"
