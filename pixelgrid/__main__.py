"""Main module."""
from pathlib import Path

import typer
from PIL import Image

from .operations import (
    NumberFont,
    compute_square_numbering,
    get_number_layer,
    get_square_layer,
    get_squares_with_pixels,
    scale10x,
)

APP = typer.Typer()


@APP.command()
def main(image: Path, numbers_path: Path, output: Path = Path("output.png")) -> None:
    """Generate pixel art diagrams."""

    with Image.open(image) as im:
        number_font = NumberFont.from_file(numbers_path)

        resized = scale10x(im)

        squares = list(get_squares_with_pixels(resized, 50))

        numbers = compute_square_numbering(squares)
        square_layer = get_square_layer(resized, squares)
        number_layer = get_number_layer(resized, numbers, number_font)

        resized.paste(square_layer, mask=square_layer)
        resized.paste(number_layer, mask=number_layer)
        resized.save(output)


APP()
