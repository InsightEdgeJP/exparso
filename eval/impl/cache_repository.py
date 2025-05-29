import os
from logging import getLogger

from eval.models import ParseDataModel, Repository

logger = getLogger(__name__)


class CacheRepository(Repository):
    cache_dir = ".cache"

    def __init__(self):
        os.makedirs(self.cache_dir, exist_ok=True)

    def get(self, id: str) -> ParseDataModel | None:
        file_path = os.path.join(self.cache_dir, f"{id}.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                logger.info(f"Load cache: {file_path}")
                return ParseDataModel.model_validate_json(f.read())
        return None

    def set(self, id: str, data: ParseDataModel):
        file_path = os.path.join(self.cache_dir, f"{id}.json")
        with open(file_path, "w") as f:
            logger.info(f"Save cache: {file_path}")
            f.write(data.model_dump_json())
