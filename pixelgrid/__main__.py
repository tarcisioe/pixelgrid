"""Main module."""
from pathlib import Path

import typer
from PIL import Image

from .operations import (
    compute_square_numbering,
    draw_square_numbering_on_image,
    draw_squares_if_pixels,
    get_squares_with_pixels,
    scale10x,
)

APP = typer.Typer()


@APP.command()
def main(image: Path, output: Path = Path("output.png")) -> None:
    """Generate pixel art diagrams."""

    with Image.open(image) as im:
        resized = scale10x(im)

        squares = list(get_squares_with_pixels(resized, 50))
        numbers = compute_square_numbering(squares)

        with_squares = draw_squares_if_pixels(resized)
        draw_square_numbering_on_image(with_squares, numbers)
        with_squares.save(output)


APP()
