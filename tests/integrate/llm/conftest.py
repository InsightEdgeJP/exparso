import pytest
from PIL import Image


@pytest.fixture
def example_image():
    img = Image.new("RGB", (100, 100), color="red")
    return img
