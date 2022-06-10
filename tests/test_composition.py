"""Tests for pixelgrid.composition."""
from functools import partial
from pathlib import Path

from PIL import Image

from pixelgrid.composition import RGBAColor
from pixelgrid.operations import Size

from .helpers import (
    assert_images_equal,
    run_operation_and_compare,
    run_operation_and_compare_list,
)


def test_make_grid(datadir: Path) -> None:
    """make_grid should produce a grid as expected."""
    from pixelgrid.composition import make_grid

    expected = Image.open(datadir / "grid-32x32-4px.png")

    grid = make_grid(
        size=Size(*expected.size),
        pitch=Size(32, 32),
        width=1,
        color=RGBAColor(0, 0, 0, 128),
    )

    grid.save("generated.png")

    assert_images_equal(grid, expected)


def test_change_alpha_of_nontransparent(datadir: Path) -> None:
    """change_alpha_of_nontransparent should change only non-transparent pixels."""
    from pixelgrid.composition import change_alpha_of_nontransparent

    run_operation_and_compare(
        original_file=datadir / "small_triangle_opaque.png",
        expected_file=datadir / "small_triangle_alpha_128_expected.png",
        operation=change_alpha_of_nontransparent,
    )


def test_change_alpha_of_nontransparent_does_nothing_to_fully_transparent_image(
    datadir: Path,
) -> None:
    """change_alpha_of_nontransparent should be idempotent with a transparent image."""
    from pixelgrid.composition import change_alpha_of_nontransparent

    run_operation_and_compare(
        original_file=datadir / "transparent_square.png",
        expected_file=datadir / "transparent_square.png",
        operation=change_alpha_of_nontransparent,
    )


def test_compose_steps(datadir: Path) -> None:
    """compose_steps should generate diagrams for each step as expected."""
    from pixelgrid.composition import compose_steps
    from pixelgrid.operations import NumberFont

    font = NumberFont.from_file(datadir / "numbers-3x5.png")

    run_operation_and_compare_list(
        original_files=[
            datadir / "test_background.png",
            datadir / "test_layer_1.png",
            datadir / "test_layer_2.png",
        ],
        expected_files=[
            datadir / "output-0.png",
            datadir / "output-1.png",
        ],
        operation=partial(compose_steps, number_font=font),
    )
