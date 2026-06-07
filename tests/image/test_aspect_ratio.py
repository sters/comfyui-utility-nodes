import pytest

from nodes.image.aspect_ratio import _PRESETS, AspectRatioPreset


def test_returns_width_height_int_tuple() -> None:
    out = AspectRatioPreset().resolve("SDXL 1:1 (1024x1024)", swap=False)
    assert out["result"] == (1024, 1024)


def test_swap_flips_orientation() -> None:
    out = AspectRatioPreset().resolve("SDXL 16:9 (1344x768)", swap=True)
    assert out["result"] == (768, 1344)


def test_swap_on_square_is_noop() -> None:
    out = AspectRatioPreset().resolve("SDXL 1:1 (1024x1024)", swap=True)
    assert out["result"] == (1024, 1024)


def test_unknown_preset_falls_back_to_square() -> None:
    out = AspectRatioPreset().resolve("totally made up", swap=False)
    assert out["result"] == (1024, 1024)


def test_ui_text_reflects_resolved_dimensions() -> None:
    out = AspectRatioPreset().resolve("SDXL 16:9 (1344x768)", swap=True)
    assert out["ui"]["text"] == ("768x1344",)


@pytest.mark.parametrize("name,dims", list(_PRESETS.items()))
def test_all_presets_are_multiples_of_64(name: str, dims: tuple[int, int]) -> None:
    # 64 is the safe stride for SDXL / Flux VAEs. A preset that violates
    # this would silently corrupt the latent grid for some samplers.
    w, h = dims
    assert w % 64 == 0, f"{name}: width {w} not a multiple of 64"
    assert h % 64 == 0, f"{name}: height {h} not a multiple of 64"


@pytest.mark.parametrize("name,dims", list(_PRESETS.items()))
def test_preset_label_matches_dimensions(name: str, dims: tuple[int, int]) -> None:
    # Guard against the label drifting from the actual numbers — the
    # label is the user-facing source of truth, so a mismatch is a bug.
    w, h = dims
    assert f"({w}x{h})" in name, f"label {name!r} doesn't end with ({w}x{h})"


@pytest.mark.parametrize("name,dims", list(_PRESETS.items()))
def test_all_presets_resolve(name: str, dims: tuple[int, int]) -> None:
    out = AspectRatioPreset().resolve(name, swap=False)
    assert out["result"] == dims
