import itertools

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def plot_drift(df: pd.DataFrame, output_path: str):
    df = df.assign(model=df["model"].str.split("@").str[0].replace("azure-document-intelligence", "azure DI"))

    # ファイル名よりカテゴリの作成、rankが50以上の時correct=1, それ以外は0
    df = (
        df.assign(category=df["file_id"].str.split("_").str[0])
        .assign(item=1)
        .assign(correct=(df["rank"] >= 50).astype(int))
    ).drop(columns=["file_id", "query", "expected", "answer", "rank"])
    # カテゴリごとにスコアを足し算
    df = df.groupby(["category", "model", "datetime"]).sum().reset_index()

    num_categories = len(df["category"].unique())

    plt.figure(figsize=(20, 10))
    cols = 2
    rows = num_categories // cols + (num_categories % cols > 0)
    linestyles = ["-", "--", "-.", ":"]
    markers = ["o", "s", "D", "^", "v", "P", "X"]
    linestyle_cycle = itertools.cycle(linestyles)
    marker_cycle = itertools.cycle(markers)
    for i, category in enumerate(df["category"].unique()):
        ax = plt.subplot(rows, cols, i + 1)
        df_category = df[df["category"] == category]
        ax.set_title(category + f"(max score:{df_category['item'].max()})")
        models = df_category["model"].unique()
        for model in models:
            marker = next(marker_cycle)
            linestyle = next(linestyle_cycle)
            ax.plot(
                df_category[df_category["model"] == model]["datetime"],
                df_category[df_category["model"] == model]["correct"],
                label=model,
                marker=marker,
                linestyle=linestyle,
                linewidth=1,
            )
            ax.set_ylim(0, df_category["item"].max() * 1.2)

        ax.legend()
        ax.set_xlabel("datetime")
        ax.set_ylabel("score")

        ax.grid()

    plt.savefig(output_path)


def plot_latest_df(df: pd.DataFrame, output_path: str):
    # ファイル名よりカテゴリの作成、rankが50以上の時correct=1, それ以外は0
    df = (
        df.assign(category=df["file_id"].str.split("_").str[0])
        .assign(item=1)
        .assign(correct=(df["rank"] >= 50).astype(int))
    ).drop(columns=["file_id", "query", "expected", "answer", "rank"])
    # カテゴリごとにスコアを足し算
    df = df.groupby(["category", "model"]).sum().reset_index()

    plt.figure(figsize=(15, 10))
    models = [m.replace("-", "\n") for m in df["model"].unique()]
    categories = df["category"].unique()

    x_ticks = np.array(range(len(models)))
    total_width = 0.8
    colors = ["b", "g", "r", "c", "m", "y", "k"]
    for i, category in enumerate(categories):
        ax = plt.subplot(2, 2, i + 1)
        df_category = df[df["category"] == category]
        ax.bar(
            x_ticks,
            df_category["correct"] / df_category["item"] * 100,
            label=category,
            width=total_width,
            color=colors,
        )
        ax.set_title(category)
        ax.grid()
        ax.set_ylim(0, 100)
        ax.set_ylabel("correct rate [%]")
        ax.set_xticks(x_ticks, models)

    plt.savefig(output_path)
