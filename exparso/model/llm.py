import base64
import copy
import json
from dataclasses import dataclass
from io import BytesIO
from typing import Sequence, TypeAlias

from langchain_core.runnables import RunnableSerializable
from pydantic_core._pydantic_core import ValidationError

from .cost import Cost
from .image import Image


class HumanMessage:
    def __init__(self, content: str, image: Image | None = None, image_low: bool = False):
        self.content = content
        self.image = copy.deepcopy(image)
        self.image_low = image_low

    @property
    def image_base64(self) -> tuple[str, str]:
        if not self.image:
            return "", ""
        img_base64 = base64.b64encode(self.image_bytes).decode("utf-8")
        return "image/png", img_base64

    @property
    def image_bytes(self) -> bytes:
        if not self.image:
            return b""

        buffered = BytesIO()
        self.image.save(buffered, format="PNG")
        return buffered.getvalue()

    def scale_image(self, scale: float):
        if not self.image:
            return
        height = int(self.image.height * scale)
        width = int(self.image.width * scale)
        self.image = self.image.resize((width, height))


@dataclass
class SystemMessage:
    content: str


class LlmResponse:
    content: dict

    def __init__(self, content: str, cost: Cost):
        if not content.startswith("{"):
            index = content.find("{")
            if index < 0:
                raise ValidationError("Content should start with '{'")
            content = content[index:]
        if not content.endswith("}"):
            index = content.rfind("}")
            if index < 0:
                raise ValidationError("Content should end with '}'")
            content = content[: index + 1]

        self.content = json.loads(content, strict=False)
        # self.contentの文字列の改行を置換する
        if isinstance(self.content, dict):
            self.content = {k: v.replace("<br>", "\n") if isinstance(v, str) else v for k, v in self.content.items()}
        self.cost = cost


LlmModel: TypeAlias = RunnableSerializable[Sequence[HumanMessage | SystemMessage], LlmResponse]
