"""Tests for pixelgrid.operations."""
from pathlib import Path

from PIL import Image

from .helpers import run_operation_and_compare


def test_scale_10x_scales_10x(datadir: Path) -> None:
    """Test that scale10x produces a perfectly 10x scaled image."""
    from pixelgrid.operations import scale10x

    run_operation_and_compare(
        original_file=datadir / "triangle.png",
        expected_file=datadir / "triangle_10x_expected.png",
        operation=scale10x,
    )


def test_draw_square_layer(datadir: Path) -> None:
    """Test that it's possible to draw squares with get_square_layer."""
    from pixelgrid.operations import get_square_layer, get_squares_with_pixels

    def draw_squares_if_pixels(image: Image.Image) -> Image.Image:
        squares = get_squares_with_pixels(image, 50)
        square_layer = get_square_layer(image, squares)

        result = image.copy()
        result.paste(square_layer, mask=square_layer)
        return result

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
    """Test that it's possible to draw numbers with get_number_layer."""
    from pixelgrid.operations import (
        NumberFont,
        Position,
        SquareNumber,
        get_number_layer,
    )

    font = NumberFont.from_file(datadir / "numbers-3x5.png")

    def draw_numbers_on_squares(image: Image.Image) -> Image.Image:
        number_layer = get_number_layer(
            image,
            numbers=[
                SquareNumber(Position(52, 52), 13),
                SquareNumber(Position(102, 52), 12),
            ],
            number_font=font,
        )

        result = image.copy()
        result.paste(number_layer, mask=number_layer)
        return result

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
    from pixelgrid.operations import (
        Position,
        Square,
        SquareNumber,
        compute_square_numbering,
    )

    squares: list[Square] = []

    assert not list(compute_square_numbering(squares))

    squares = [
        Square(Position(0, 0), 50),
        Square(Position(0, 50), 50),
        Square(Position(50, 0), 50),
    ]

    assert list(compute_square_numbering(squares)) == [
        SquareNumber(Position(2, 2), 0),
        SquareNumber(Position(2, 52), 1),
        SquareNumber(Position(52, 2), 2),
    ]
