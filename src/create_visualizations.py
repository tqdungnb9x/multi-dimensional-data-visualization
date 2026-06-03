"""
create_visualizations.py

Generate four 300-DPI multidimensional visualizations for the
Data Management and Visualization assignment.

Datasets
--------
1. weather_data.csv: daily weather observations by New Zealand city.
2. global_temp.csv: NASA GISS monthly global temperature anomalies.
3. minnesota_weather.csv: monthly Minnesota weather observations by site.

Outputs are written to the project's output/ directory:
- weather_heatmap.png
- weather_scatter.png
- global_temp_heatmap.png
- minnesota_precip_line.png
"""

from __future__ import annotations

import os
from typing import List

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
import seaborn as sns


MONTH_LABELS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


sns.set_theme(style="whitegrid", context="notebook")


def ensure_output_dir(path: str) -> None:
    """Create output directory if it does not already exist."""
    os.makedirs(path, exist_ok=True)


def save_figure(filename: str, outdir: str) -> str:
    """Save the current Matplotlib figure at 300 DPI and close it."""
    path = os.path.join(outdir, filename)
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()
    return path


def plot_weather_heatmap(df: pd.DataFrame, outdir: str) -> str:
    """Create a heatmap of average temperature by city and month.

    The chart uses three dimensions: city, month, and average temperature.
    """
    weather = df.copy()
    weather["month"] = pd.to_numeric(weather["month"], errors="coerce")
    weather["avg_temp"] = pd.to_numeric(weather["avg_temp"], errors="coerce")

    monthly_temp = (
        weather.dropna(subset=["city", "month", "avg_temp"])
        .groupby(["city", "month"], as_index=False)["avg_temp"]
        .mean()
    )

    heatmap_data = monthly_temp.pivot(index="city", columns="month", values="avg_temp")
    heatmap_data = heatmap_data.reindex(columns=range(1, 13))

    plt.figure(figsize=(10, 4))
    ax = sns.heatmap(
        heatmap_data,
        cmap="coolwarm",
        annot=True,
        fmt=".1f",
        linewidths=0.5,
        linecolor="white",
        cbar_kws={"label": "Average temperature (°F)"},
    )
    ax.set_title("Average monthly temperature by city", fontsize=14, weight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("City")
    ax.set_xticklabels(MONTH_LABELS, rotation=45, ha="right")

    return save_figure("weather_heatmap.png", outdir)


def plot_weather_scatter(df: pd.DataFrame, outdir: str) -> str:
    """Create a scatter plot of humidity, temperature, precipitation, and city.

    Dimensions shown: humidity on X, temperature on Y, city by color,
    and precipitation by marker size.
    """
    weather = df.copy()
    numeric_columns = ["avg_humidity", "avg_temp", "precip"]
    for column in numeric_columns:
        weather[column] = pd.to_numeric(weather[column], errors="coerce")
    weather["precip"] = weather["precip"].fillna(0.0)
    weather = weather.dropna(subset=["avg_humidity", "avg_temp", "city"])

    size_range = (20, 300)
    city_order = sorted(weather["city"].unique())
    palette = dict(zip(city_order, sns.color_palette("tab10", n_colors=len(city_order))))

    plt.figure(figsize=(9, 6))
    ax = sns.scatterplot(
        data=weather,
        x="avg_humidity",
        y="avg_temp",
        hue="city",
        hue_order=city_order,
        palette=palette,
        size="precip",
        sizes=size_range,
        alpha=0.65,
        edgecolor="none",
        legend=False,
    )

    city_handles = [
        Line2D([0], [0], marker="o", linestyle="", label=city, markerfacecolor=palette[city], markeredgecolor="none", markersize=8)
        for city in city_order
    ]
    city_legend = ax.legend(handles=city_handles, title="City", loc="upper left", bbox_to_anchor=(1.02, 1.0), frameon=True)
    ax.add_artist(city_legend)

    max_precip = float(weather["precip"].max())
    precip_values = np.linspace(0, max_precip, 4) if max_precip > 0 else np.array([0.0])
    precip_handles = []
    for value in precip_values:
        size = np.interp(value, [0, max_precip], size_range) if max_precip > 0 else size_range[0]
        precip_handles.append(plt.scatter([], [], s=size, color="gray", alpha=0.65, label=f"{value:.2f}"))
    ax.legend(handles=precip_handles, title="Precipitation", loc="lower left", bbox_to_anchor=(1.02, 0.0), frameon=True)

    ax.set_title("Daily weather: temperature vs humidity with precipitation (size)", fontsize=14, weight="bold")
    ax.set_xlabel("Average relative humidity (%)")
    ax.set_ylabel("Average temperature (°F)")

    return save_figure("weather_scatter.png", outdir)


def plot_global_temp_heatmap(df: pd.DataFrame, outdir: str) -> str:
    """Create a heatmap of global monthly temperature anomalies by year."""
    global_temp = df.copy()
    month_map = {month: index + 1 for index, month in enumerate(MONTH_LABELS)}

    global_long = global_temp.melt(
        id_vars="Year",
        value_vars=MONTH_LABELS,
        var_name="Month",
        value_name="Anomaly",
    )
    global_long["MonthNum"] = global_long["Month"].map(month_map)
    global_long["Year"] = pd.to_numeric(global_long["Year"], errors="coerce")
    global_long["Anomaly"] = pd.to_numeric(global_long["Anomaly"], errors="coerce")

    heatmap_data = global_long.pivot(index="Year", columns="MonthNum", values="Anomaly").sort_index()

    plt.figure(figsize=(10, 8))
    ax = sns.heatmap(
        heatmap_data,
        cmap="coolwarm",
        vmin=-1.5,
        vmax=1.5,
        linewidths=0,
        linecolor="white",
        cbar_kws={"label": "Temperature anomaly (°C relative to 1951–1980)"},
    )
    ax.set_title("Global land–ocean temperature anomalies (1880–2025)", fontsize=14, weight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Year")
    ax.set_xticklabels(MONTH_LABELS, rotation=45, ha="right")

    # Show fewer y-axis labels so the long 1880-2025 heatmap remains readable.
    year_labels = heatmap_data.index.to_numpy(dtype=int)
    tick_positions = np.arange(0.5, len(year_labels), 10)
    ax.set_yticks(tick_positions)
    ax.set_yticklabels(year_labels[::10], rotation=0)

    return save_figure("global_temp_heatmap.png", outdir)


def plot_minnesota_precip_line(df: pd.DataFrame, outdir: str) -> str:
    """Create a monthly precipitation line chart by Minnesota site."""
    minnesota = df.copy()
    minnesota["year"] = pd.to_numeric(minnesota["year"], errors="coerce")
    minnesota["mo"] = pd.to_numeric(minnesota["mo"], errors="coerce")
    minnesota["precip"] = pd.to_numeric(minnesota["precip"], errors="coerce")
    minnesota = minnesota.dropna(subset=["site", "year", "mo", "precip"])
    minnesota["date"] = pd.to_datetime(
        dict(year=minnesota["year"].astype(int), month=minnesota["mo"].astype(int), day=1)
    )

    monthly_site_precip = (
        minnesota.groupby(["site", "date"], as_index=False)["precip"]
        .mean()
        .sort_values(["site", "date"])
    )

    plt.figure(figsize=(10, 6))
    ax = sns.lineplot(data=monthly_site_precip, x="date", y="precip", hue="site", marker="o", linewidth=1.4, markersize=3)
    ax.set_title("Monthly precipitation by Minnesota site (1927–1936)", fontsize=14, weight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("Precipitation (inches)")
    ax.legend(title="Site", bbox_to_anchor=(1.05, 1), loc="upper left", frameon=True)

    return save_figure("minnesota_precip_line.png", outdir)


def main() -> List[str]:
    """Load datasets, generate all figures, and return generated paths."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    out_dir = os.path.join(base_dir, "output")
    ensure_output_dir(out_dir)

    figures: List[str] = []

    weather_path = os.path.join(data_dir, "weather_data.csv")
    weather_df = pd.read_csv(weather_path)
    figures.append(plot_weather_heatmap(weather_df, out_dir))
    figures.append(plot_weather_scatter(weather_df, out_dir))

    global_path = os.path.join(data_dir, "global_temp.csv")
    global_df = pd.read_csv(global_path, skiprows=1).replace("***", pd.NA)
    for column in global_df.columns[1:]:
        global_df[column] = pd.to_numeric(global_df[column], errors="coerce")
    figures.append(plot_global_temp_heatmap(global_df, out_dir))

    minnesota_path = os.path.join(data_dir, "minnesota_weather.csv")
    minnesota_df = pd.read_csv(minnesota_path)
    figures.append(plot_minnesota_precip_line(minnesota_df, out_dir))

    return figures


if __name__ == "__main__":
    generated_files = main()
    print("Generated figures:")
    for generated_file in generated_files:
        print(generated_file)
