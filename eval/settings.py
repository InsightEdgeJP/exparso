import os
from datetime import datetime

import pandas as pd
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from eval.models import FileModel, QueryModel


class Settings(BaseSettings):
    model_config: SettingsConfigDict = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
        "case_sensitive": True,
    }
    setting_xlsx_path: str = "eval/data/setting.xlsx"
    eval_data_dir: str = "eval/data"
    result_excel_path: str = "eval/data/result/result.xlsx"
    result_latest_plot_path: str = "eval/data/result/summary.png"
    result_drift_plot_path: str = "eval/data/result/drift.png"

    # GCS
    gcs_bucket: str = "parse-docs-lib"
    benchmark_blob_name: str = "eval/benchmark.xlsx"

    environment: str = Field(alias="ENVIRONMENT", default="local")

    result_drift_plot_blob: str = "eval/result/drift.png"
    result_latest_plot_blob: str = "eval/result/summary.png"

    result_blob_prefix: str = "eval/result/"
    result_blob_name: str = "eval/result/result_{date}.xlsx".format(date=datetime.now().strftime("%Y%m%d%H%M%S"))

    gcp_project: str = Field(alias="GCP_PROJECT", default="")
    azure_document_endpoint: str = Field(alias="AZURE_DOCUMENT_ENDPOINT", default="")

    langfuse_secret_key: str = Field(alias="LANGFUSE_SECRET_KEY", default="")
    langfuse_public_key: str = Field(alias="LANGFUSE_PUBLIC_KEY", default="")
    langfuse_host: str = Field(alias="LANGFUSE_HOST", default="")

    @property
    def eval_blob_prefix(self) -> str:
        return "eval/image/stage" if self.environment != "main" else "eval/image/main"


def load_setting_xlsx() -> list[QueryModel]:
    file_path = settings.setting_xlsx_path

    query_pd = pd.read_excel(file_path, sheet_name="query")
    queries = [QueryModel(**row) for row in query_pd.to_dict(orient="records")]  # type: ignore
    file_ids: list[str] = [row["file_id"] for row in query_pd.to_dict(orient="records")]

    for q, f in zip(queries, file_ids):
        q.file = FileModel(path=os.path.join(settings.eval_data_dir, f), id=f)
    return queries


settings = Settings()
