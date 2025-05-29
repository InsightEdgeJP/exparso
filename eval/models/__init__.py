import hashlib
from abc import abstractmethod

from pydantic import BaseModel


class FileModel(BaseModel):
    path: str
    id: str


class QueryModel(BaseModel):
    query: str
    expected: str
    page_number: int
    file: FileModel = FileModel(path="", id="")

    @property
    def query_id(self) -> str:
        return hashlib.md5(self.query.encode()).hexdigest()

    @property
    def display_file_id(self) -> str:
        return self.file.id.split(".")[0]


class EvalDataModel(BaseModel):
    query: str
    expected: str
    answer: str
    rank: int
    file_id: str
    model: str


class ParseDataModel(BaseModel):
    file_id: str
    model: str
    document: list[str]
    evals: dict[str, EvalDataModel] = {}


class Repository:
    @abstractmethod
    def get(self, id: str) -> ParseDataModel | None:
        pass

    @abstractmethod
    def set(self, id: str, data: ParseDataModel):
        pass


class Parser:

    @abstractmethod
    def parse(self, file: FileModel) -> ParseDataModel:
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        pass
