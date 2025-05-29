from PIL import Image as PILImage

from exparso.model import HumanMessage


def test_human_message():
    message = HumanMessage(content="Hello, World!")
    assert message.content == "Hello, World!"
    assert message.image is None


def test_human_with_image():
    image = PILImage.new("RGB", (100, 100))
    message = HumanMessage(content="Hello, World!", image=image)
    assert message.content == "Hello, World!"
    image_type, base64 = message.image_base64
    assert image_type.startswith("image/png")
    assert base64
    assert message.image_bytes


def test_human_with_image_low():
    image = PILImage.new("RGB", (160, 100))
    message = HumanMessage(content="Hello, World!", image=image, image_low=True)
    assert message.image
    assert message.image.height == 100
    assert message.image.width == 160
    message.scale_image(0.5)
    assert message.image.height == 50
    assert message.image.width == 80
