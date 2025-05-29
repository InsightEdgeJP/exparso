import pandas as pd
from langchain_core.language_models.chat_models import BaseChatModel
from tqdm import tqdm

from eval.impl import (
    AzureDocumentIntelligence,
    CacheRepository,
    Docling,
    Exparso,
    GCSHelper,
    Pymupdf4llm,
    create_llm,
    plot_drift,
    plot_latest_df,
)
from eval.models import Parser, QueryModel
from eval.settings import load_setting_xlsx, settings
from eval.usecase import Evaluator


def run_eval(queries: list[QueryModel], models: list[Parser], llm: BaseChatModel) -> pd.DataFrame:
    pattern: list[tuple[Parser, QueryModel]] = [(m, q) for m in models for q in queries]
    df = pd.DataFrame(columns=["model", "file_id", "query", "expected", "answer", "rank"])
    repository = CacheRepository()
    for m, q in tqdm(pattern, desc="Evaluating queries"):
        eval_data = Evaluator(parser=m, query=q, repository=repository).eval(llm)
        new_df = pd.DataFrame([{**eval_data.model_dump()}])
        df = pd.concat([df, new_df], ignore_index=True)

    return df


def history(gcs_helper: GCSHelper, result_prefix: str) -> pd.DataFrame:
    history_data = gcs_helper.get_blob_list(result_prefix)
    history_dfs = [
        gcs_helper.download_blob_to_df(blob_name).assign(
            datetime=pd.to_datetime(blob_name.split(".")[0].split("_")[-1])
        )
        for blob_name in history_data
    ]
    df = pd.concat(history_dfs, ignore_index=True)
    return df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the evaluation")
    parser.add_argument("--benchmark", help="Benchmark", action="store_true")
    parser.add_argument("--save-gcs", help="Save gcs result", action="store_true")

    args = parser.parse_args()

    print("Loading setting...")
    queries = load_setting_xlsx()

    llm = create_llm()
    parse_lib = Exparso(model=llm, model_name="gemini-1.5-pro-002")

    gcs_helper = GCSHelper(bucket_name=settings.gcs_bucket)

    if args.benchmark:
        models = [Pymupdf4llm(), AzureDocumentIntelligence(), Docling()]
        df = run_eval(queries=queries, models=models, llm=llm)
        gcs_helper.upload_df_to_blob(df=df, blob_name=settings.benchmark_blob_name)

    benchmark_df = gcs_helper.download_blob_to_df(settings.benchmark_blob_name)
    df = run_eval(queries=queries, models=[parse_lib], llm=llm)

    df = pd.concat([benchmark_df, df], ignore_index=True)
    df.to_excel(settings.result_excel_path, index=False)

    plot_latest_df(df, settings.result_latest_plot_path)

    if args.save_gcs:
        df = pd.read_excel(settings.result_excel_path)
        gcs_helper.upload_df_to_blob(df=df, blob_name=settings.result_blob_name)
        gcs_helper.upload_file_to_blob(settings.result_latest_plot_path, settings.result_latest_plot_blob)

        df = history(gcs_helper, settings.result_blob_prefix)
        drift = plot_drift(df, settings.result_drift_plot_path)
        gcs_helper.upload_file_to_blob(settings.result_drift_plot_path, settings.result_drift_plot_blob)
