"""Module with image manipulation operations."""
from typing import Iterable, Iterator, Literal, NamedTuple

from PIL import Image, ImageDraw


class Position(NamedTuple):
    """Represent the position of a given pixel."""

    x: int
    y: int


def scale10x(image: Image.Image) -> Image.Image:
    """Scale an image by 10 times."""

    width, height = image.size

    new_size = (width * 10, height * 10)

    resampling: Literal[0] = Image.Resampling.NEAREST  # type: ignore

    return image.resize(new_size, resample=resampling)


def check_pixels_in_square(
    image: Image.Image, x_origin: int, y_origin: int, square_size: int
) -> bool:
    """Check if there are any opaque pixels in a given square."""
    for y in range(y_origin, y_origin + square_size):
        for x in range(x_origin, x_origin + square_size):
            (_, _, _, alpha) = image.getpixel((x, y))
            if alpha == 255:
                return True

    return False


def get_squares_with_pixels(
    image: Image.Image,
    square_size: int,
) -> Iterator[Position]:
    """Yield every square where there is at least one fully opaque pixel."""
    for y in range(0, image.height, square_size):
        for x in range(0, image.width, square_size):
            if check_pixels_in_square(image, x, y, square_size):
                yield Position(x, y)


def draw_squares_on_image(
    image: Image.Image,
    squares: Iterable[Position],
    square_size: int,
) -> None:
    """Draw a given collection of squares on an image."""
    drawer = ImageDraw.Draw(image)

    for x, y in squares:
        drawer.rectangle(
            ((x, y), (x + square_size, y + square_size)),
            outline=(0, 0, 0),
            width=1,
        )


def draw_squares_if_pixels(image: Image.Image) -> Image.Image:
    """Draw 50x50 squares wherever there are pixels in the original image."""
    square_size = 50

    squares = get_squares_with_pixels(image, square_size)
    result = image.copy()

    draw_squares_on_image(result, squares, square_size)

    return result
