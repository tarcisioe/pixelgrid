"""Functions that compose images into diagrams."""
from typing import Iterable, NamedTuple

from PIL import Image, ImageDraw

from .operations import (
    NumberFont,
    Position,
    Size,
    compute_square_numbering,
    get_number_layer,
    get_square_layer,
    get_squares_with_pixels,
    scale10x,
)


class RGBAColor(NamedTuple):
    """Represent a color in RGBA colorspace."""

    r: int
    g: int
    b: int
    a: int = 255


def make_grid(
    *,
    size: Size,
    pitch: Size,
    width: int,
    color: RGBAColor,
) -> Image.Image:
    """Draw a grid given parameters.

    Args:
        size: The size of the whole grid.
        pitch: The size of each grid cell.
        width: The width of the lines.
        color: Which color to color the grid with.

    Returns:
        The generated grid.
    """
    grid = Image.new("RGBA", size, (0, 0, 0, 0))

    drawer = ImageDraw.Draw(grid)

    for y in range(0, size.height, pitch.height):
        drawer.line((Position(0, y), Position(size.width, y)), width=width, fill=color)

    for x in range(0, size.width, pitch.width):
        drawer.line((Position(x, 0), Position(x, size.height)), width=width, fill=color)

    return grid


def change_alpha_of_nontransparent(image: Image.Image) -> Image.Image:
    """Change alpha of every non-transparent pixel of an image to 128.

    Args:
        image: The original image.

    Returns:
        The transformed image.
    """
    result = image.copy()
    alpha = result.getchannel("A")

    new_alpha = alpha.point(lambda i: 128 if i > 0 else 0)
    result.putalpha(new_alpha)

    return result


def alpha_composite(images: Iterable[Image.Image]) -> Image.Image:
    """Create the alpha-composition of a collection of images.

    Same as "merge visible layers" in image editors.

    Args:
        images: The list of images to composite.

    Returns:
        The final merged image.
    """
    background, *layers = images

    result = background.copy()

    for layer in layers:
        result.alpha_composite(layer)

    return result


def create_diagram(
    background: Image.Image,
    new_layer: Image.Image,
    grid: Image.Image,
    already_drawn: list[Image.Image],
    number_font: NumberFont,
) -> Image.Image:
    """Create a single diagram.

    Args:
        background: The background image.
        new_layer: The layer being added to the image.
        grid: The pixel grid.
        already_drawn: The layers that were already drawn.
        number_font: The font to use for writing numbers on squares.
    """
    squares = list(get_squares_with_pixels(new_layer, 50))
    numbers = compute_square_numbering(squares)
    square_layer = get_square_layer(new_layer, squares)
    number_layer = get_number_layer(new_layer, numbers, number_font)

    white_background = Image.new(
        mode="RGBA",
        size=background.size,
        color=RGBAColor(255, 255, 255, 255),
    )

    previous_steps_background = alpha_composite(
        [
            background,
            *already_drawn,
        ]
    )

    return alpha_composite(
        [
            white_background,
            change_alpha_of_nontransparent(previous_steps_background),
            new_layer,
            square_layer,
            number_layer,
            grid,
        ]
    )


def compose_steps(
    images: list[Image.Image], number_font: NumberFont
) -> list[Image.Image]:
    """Compose a series of diagrams given a list of steps.

    Args:
        images: The image of every step of the pixel art.
        number_font: The font to use for writing numbers on squares.

    Returns:
        A list of diagrams for every step.
    """
    images10x = [scale10x(im) for im in images]

    background, *layers = images10x

    grid = make_grid(
        size=Size(*background.size),
        pitch=Size(10, 10),
        width=1,
        color=RGBAColor(0, 0, 0, 50),
    )

    already_drawn: list[Image.Image] = []

    outputs: list[Image.Image] = []

    for image in layers:
        outputs.append(
            create_diagram(background, image, grid, already_drawn, number_font)
        )
        already_drawn.append(image)

    return outputs
