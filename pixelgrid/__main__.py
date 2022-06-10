"""Main module."""
from contextlib import ExitStack
from pathlib import Path
from typing import List

import typer
from PIL import Image

from .composition import compose_steps
from .operations import NumberFont

APP = typer.Typer()


@APP.command()
def main(
    layers: List[Path], numbers_path: Path, output: Path = Path("output.png")
) -> None:
    """Generate pixel art diagrams."""
    number_font = NumberFont.from_file(numbers_path)

    with ExitStack() as ex:
        images = [ex.enter_context(Image.open(layer)) for layer in layers]

        outputs = compose_steps(images, number_font)

        for i, im in enumerate(outputs):
            directory = output.parent
            im.save(directory / f"{output.stem}-{i}{output.suffix}")


APP()
