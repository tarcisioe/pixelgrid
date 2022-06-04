"""Main module."""
from pathlib import Path

import typer
from PIL import Image

from .operations import draw_squares_if_pixels, scale10x

APP = typer.Typer()


@APP.command()
def main(image: Path, output: Path = Path("output.png")) -> None:
    """Generate pixel art diagrams."""

    with Image.open(image) as im:
        resized = scale10x(im)
        with_squares = draw_squares_if_pixels(resized)
        with_squares.save(output)


APP()
