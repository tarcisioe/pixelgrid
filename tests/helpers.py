"""Helper module for tests with images."""
from contextlib import ExitStack
from pathlib import Path
from typing import Callable

from PIL import Image, ImageChops


def assert_images_equal(image1: Image.Image, image2: Image.Image) -> None:
    """Assert that two images are the same."""
    diff = ImageChops.difference(image1, image2)
    assert not diff.getbbox()


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
