"""Functions that compose images into diagrams."""
from typing import NamedTuple

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
        color=RGBAColor(0, 0, 0, 128),
    )

    already_drawn: list[Image.Image] = []

    outputs: list[Image.Image] = []

    for image in layers:
        squares = list(get_squares_with_pixels(image, 50))
        numbers = compute_square_numbering(squares)
        square_layer = get_square_layer(image, squares)
        number_layer = get_number_layer(image, numbers, number_font)

        result = background.convert("RGBA")

        for previous in already_drawn:
            result.alpha_composite(previous)

        result.paste(image, mask=image)

        result.paste(square_layer, mask=square_layer)
        result.paste(number_layer, mask=number_layer)

        result.alpha_composite(grid)
        already_drawn.append(change_alpha_of_nontransparent(image))
        outputs.append(result)

    return outputs
