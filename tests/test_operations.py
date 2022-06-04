"""Tests for pixelgrid.operations."""
from pathlib import Path
from typing import Callable

from PIL import Image, ImageChops


def run_operation_and_compare(
    original_file: Path,
    expected_file: Path,
    operation: Callable[[Image.Image], Image.Image],
) -> None:
    """Run an operation on an image and check if the result is as expected."""
    with Image.open(original_file) as im:
        processed = operation(im)

    with Image.open(expected_file) as expected:
        diff = ImageChops.difference(processed, expected)

    assert not diff.getbbox()


def test_scale_10x_scales_10x(datadir: Path) -> None:
    """Test that scale10x produces a perfectly 10x scaled image."""
    from pixelgrid.operations import scale10x

    run_operation_and_compare(
        original_file=datadir / "triangle.png",
        expected_file=datadir / "triangle_10x_expected.png",
        operation=scale10x,
    )


def test_draw_squares_if_pixels_draws_squares(datadir: Path) -> None:
    """Test that draw_squares_if_pixels draws squares if it should."""
    from pixelgrid.operations import draw_squares_if_pixels

    run_operation_and_compare(
        original_file=datadir / "triangle_10x_expected.png",
        expected_file=datadir / "triangle_10x_with_squares_expected.png",
        operation=draw_squares_if_pixels,
    )
