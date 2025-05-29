from PIL import Image

from ..model import LoadPageContents, PageLoader


class ImageLoader(PageLoader):
    def load(self, path: str) -> list[LoadPageContents]:
        with Image.open(path) as im:
            image = im.convert("RGB")
        return [
            LoadPageContents(
                contents="",
                page_number=0,
                image=image,
                tables=[],
            )
        ]
