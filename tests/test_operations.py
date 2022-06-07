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


def test_draw_number(datadir: Path) -> None:
    """Test that draw_number writes a number on the correct position."""
    from pixelgrid.operations import NumberFont, Position, draw_number

    font = NumberFont.from_file(datadir / "numbers-3x5.png")

    def draw_number_on_image(image: Image.Image) -> Image.Image:
        draw_number(
            image,
            1917,
            Position(10, 10),
            spacing=1,
            number_font=font,
        )

        return image

    run_operation_and_compare(
        original_file=datadir / "white_square.png",
        expected_file=datadir / "square_with_number.png",
        operation=draw_number_on_image,
    )


def test_draw_square_numbering_on_image(datadir: Path) -> None:
    """Test that draw_square_numbering_on_image draws the numbers correctly."""
    from pixelgrid.operations import (
        NumberFont,
        Position,
        SquareNumber,
        draw_square_numbering_on_image,
    )

    font = NumberFont.from_file(datadir / "numbers-3x5.png")

    def draw_numbers_on_squares(image: Image.Image) -> Image.Image:
        draw_square_numbering_on_image(
            image,
            numbers=[
                SquareNumber(Position(52, 52), 13),
                SquareNumber(Position(102, 52), 12),
            ],
            number_font=font,
        )

        return image

    run_operation_and_compare(
        original_file=datadir / "squares_unnumbered.png",
        expected_file=datadir / "squares_numbered.png",
        operation=draw_numbers_on_squares,
    )


def test_number_font_get_digit(datadir: Path) -> None:
    """Test that NumberFont.get_digit return a correctly cropped digit."""
    from pixelgrid.operations import NumberFont, Size

    def get_digit_using_number_font(numbers_image: Image.Image) -> Image.Image:
        font = NumberFont(numbers_image, Size(3, 5))
        return font.get_digit(3)

    run_operation_and_compare(
        original_file=datadir / "numbers-3x5.png",
        expected_file=datadir / "three.png",
        operation=get_digit_using_number_font,
    )


def test_number_font_from_file(datadir: Path) -> None:
    """Test that NumberFont.get_digit return a correctly cropped digit."""
    from pixelgrid.operations import NumberFont, Size

    assert NumberFont.from_file(datadir / "numbers-3x5.png").size == Size(3, 5)


def test_compute_square_numbering() -> None:
    """Test that compute_square_numbering computes the proper positions and numbers."""
    from pixelgrid.operations import Position, SquareNumber, compute_square_numbering

    squares: list[Position] = []

    assert not list(compute_square_numbering(squares))

    squares = [
        Position(0, 0),
        Position(0, 50),
        Position(50, 0),
    ]

    assert list(compute_square_numbering(squares)) == [
        SquareNumber(Position(2, 2), 0),
        SquareNumber(Position(2, 52), 1),
        SquareNumber(Position(52, 2), 2),
    ]
