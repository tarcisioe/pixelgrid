"""Main module."""
from pathlib import Path

import typer
from PIL import Image

from .operations import scale10x

APP = typer.Typer()


@APP.command()
def main(image: Path, output: Path = Path("output.png")) -> None:
    """Generate pixel art diagrams."""

    with Image.open(image) as im:
        resized = scale10x(im)
        resized.save(output)


APP()
