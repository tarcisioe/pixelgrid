"""Tests for pixelgrid.operations."""
from pathlib import Path

from PIL import Image, ImageChops

from pixelgrid.operations import scale10x


def test_scale_10x_scales_10x(datadir: Path) -> None:
    """Test that scale10x produces a perfectly 10x scaled image."""
    original_file = datadir / "triangle.png"
    expected_file = datadir / "triangle_10x_expected.png"

    with Image.open(original_file) as im:
        scaled = scale10x(im)

    with Image.open(expected_file) as expected:
        diff = ImageChops.difference(scaled, expected)

    assert not diff.getbbox()
