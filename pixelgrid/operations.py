"""Module with image manipulation operations."""
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Literal, NamedTuple, Sequence

from PIL import Image, ImageChops, ImageDraw


class Size(NamedTuple):
    """Represent a size in two dimensions."""

    width: int
    height: int


class Delta(NamedTuple):
    """Represent a distance between positions."""

    dx: int
    dy: int


class Position(NamedTuple):
    """Represent the position of a given pixel."""

    x: int
    y: int

    def translate(self, delta: Delta) -> "Position":
        """Compute a translated version of this position."""
        return Position(
            x=self.x + delta.dx,
            y=self.y + delta.dy,
        )


def scale10x(image: Image.Image) -> Image.Image:
    """Scale an image by 10 times."""

    width, height = image.size

    new_size = (width * 10, height * 10)

    resampling: Literal[0] = Image.Resampling.NEAREST  # type: ignore

    return image.resize(new_size, resample=resampling)


def check_pixels_in_square(
    image: Image.Image, origin: Position, square_size: int
) -> bool:
    """Check if there are any opaque pixels in a given square."""
    transparent = Image.new("RGBA", (square_size, square_size), color=(0, 0, 0, 0))
    box_end = origin.translate(Delta(square_size - 1, square_size - 1))
    square = image.crop((*origin, *box_end))
    diff = ImageChops.difference(transparent, square)
    return bool(diff.getbbox())


def get_squares_with_pixels(
    image: Image.Image,
    square_size: int,
) -> Iterator[Position]:
    """Yield every square where there is at least one fully opaque pixel."""
    for y in range(0, image.height, square_size):
        for x in range(0, image.width, square_size):
            square_corner = Position(x, y)
            if check_pixels_in_square(image, square_corner, square_size):
                yield square_corner


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


@dataclass
class SquareNumber:
    """The numbering for each square we want to draw."""

    position: Position
    value: int


def compute_square_numbering(
    squares: Sequence[Position],
) -> Iterator[SquareNumber]:
    """Compute where to draw the numbers of a sequence of squares."""

    for number, square_position in enumerate(squares):
        yield SquareNumber(
            position=square_position.translate(Delta(2, 2)),
            value=number,
        )


def draw_squares_if_pixels(image: Image.Image) -> Image.Image:
    """Draw 50x50 squares wherever there are pixels in the original image."""
    square_size = 50

    squares = get_squares_with_pixels(image, square_size)
    result = image.copy()

    draw_squares_on_image(result, squares, square_size)

    return result


@dataclass
class NumberFont:
    """A simple pixel-based font containing only numbers."""

    pixels: Image.Image
    size: Size

    def get_digit(self, digit: int) -> Image.Image:
        """Get the image of a given digit."""
        delta_start = Delta(self.size.width * digit, 0)
        position = Position(0, 0).translate(delta_start)
        delta_end = Delta(*self.size)
        end = position.translate(delta_end)
        return self.pixels.crop((*position, *end))

    @staticmethod
    def from_file(image: Path) -> "NumberFont":
        """Get a NumberFont object from a given image file.

        The file should be called name-WxH where W is the
        width of each digit and H is the height.
        """
        _, size_txt = image.stem.split("-", maxsplit=1)
        size_numbers = size_txt.split("x", maxsplit=1)
        size = Size(*(int(n) for n in size_numbers))

        with Image.open(image) as im:
            return NumberFont(
                pixels=im.convert("RGBA"),
                size=size,
            )


def draw_number(
    image: Image.Image,
    number: int,
    position: Position,
    spacing: int,
    number_font: NumberFont,
) -> None:
    """Draw a number digit by digit on an image.

    Args:
        image: The image where to draw the numbers.
        number: The number to write.
        position: Where to write the number.
        spacing: How much horizontal spacing to add between each digit.
        number_font: A NumberFont object with the loaded digit "font" image.
    """
    digits = (int(c) for c in str(number))

    digit_position = position

    for digit in digits:
        digit_image = number_font.get_digit(digit)
        image.paste(digit_image, digit_position, mask=digit_image)
        digit_position = digit_position.translate(
            Delta(number_font.size.width + spacing, 0)
        )


def draw_square_numbering_on_image(
    image: Image.Image,
    numbers: Iterable[SquareNumber],
    number_font: NumberFont,
) -> None:
    """Draw a given collection of squares on an image."""
    for number in numbers:
        position = number.position

        draw_number(
            image,
            number.value,
            position,
            1,
            number_font,
        )
