"""Module with image manipulation operations."""
from typing import Literal

from PIL import Image


def scale10x(image: Image.Image) -> Image.Image:
    """Scale an image by 10 times."""

    width, height = image.size

    new_size = (width * 10, height * 10)

    resampling: Literal[0] = Image.Resampling.NEAREST  # type: ignore

    return image.resize(new_size, resample=resampling)
