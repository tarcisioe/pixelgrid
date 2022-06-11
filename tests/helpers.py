"""Helper module for tests with images."""
from contextlib import ExitStack
from pathlib import Path
from typing import Callable

from PIL import Image, ImageChops


def assert_images_equal(image1: Image.Image, image2: Image.Image) -> None:
    """Assert that two images are the same."""
    equal_size = image1.height == image2.height and image1.width == image2.width

    image1 = image1.convert("RGBA")
    image2 = image2.convert("RGBA")

    alpha_1 = image1.getchannel("A")
    alpha_2 = image2.getchannel("A")

    equal_alphas = not ImageChops.difference(alpha_1, alpha_2).getbbox()

    equal_content = not ImageChops.difference(
        image1.convert("RGB"), image2.convert("RGB")
    ).getbbox()

    assert equal_size and equal_alphas and equal_content


def run_operation_and_compare_list(
    original_files: list[Path],
    expected_files: list[Path],
    operation: Callable[[list[Image.Image]], list[Image.Image]],
) -> None:
    """Run an operation on an image and check if the result is as expected."""
    with ExitStack() as ex:
        images = [ex.enter_context(Image.open(file)) for file in original_files]
        processed = operation(images)

    with ExitStack() as ex:
        expecteds = [ex.enter_context(Image.open(file)) for file in expected_files]

        assert len(processed) == len(expecteds)

        for result, expected in zip(processed, expecteds):
            assert_images_equal(result, expected)


def run_operation_and_compare(
    original_file: Path,
    expected_file: Path,
    operation: Callable[[Image.Image], Image.Image],
) -> None:
    """Run an operation on an image and check if the result is as expected."""

    def run_operation_with_list(original: list[Image.Image]) -> list[Image.Image]:
        (only,) = original

        return [operation(only)]

    run_operation_and_compare_list(
        [original_file], [expected_file], run_operation_with_list
    )
