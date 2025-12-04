import os
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import matplotlib.pyplot as plt

from config import FINAL_DATA_CSV, FINAL_DATA_CLEAN_CSV


def load_and_clean_final_data(
    input_path: str = FINAL_DATA_CSV,
    output_path: str = FINAL_DATA_CLEAN_CSV,
) -> pd.DataFrame:
    """
    Load the merged ZIP-level dataset, clean variables, and save a cleaned version.
    Returns the cleaned DataFrame.
    """

    # Load final_data.csv
    final_data = pd.read_csv(input_path)

    # ONE: Clean up NAME cols: keep one readable name column
    if "NAME_x" in final_data.columns and "NAME_y" in final_data.columns:
        final_data = final_data.drop(columns=["NAME_x"])
        final_data = final_data.rename(columns={"NAME_y": "zcta_name"})
    elif "NAME_x" in final_data.columns:
        final_data = final_data.rename(columns={"NAME_x": "zcta_name"})
    elif "NAME_y" in final_data.columns:
        final_data = final_data.rename(columns={"NAME_y": "zcta_name"})

    # TWO: Ensure commute column is numeric
    final_data["mean_commute_time"] = pd.to_numeric(
        final_data.get("mean_commute_time"), errors="coerce"
    )

    # THREE: Detect whether values are still scaled (raw ACS) and divide by 1000 if needed.
    commute_median = final_data["mean_commute_time"].median(skipna=True)
    print("median before possible scaling:", commute_median)

    if pd.notna(commute_median) and commute_median > 100:
        print("Dividing mean_commute_time by 1000 to convert to minutes...")
        final_data["mean_commute_time"] = final_data["mean_commute_time"] / 1000.0
    else:
        print("Values look already in minutes (no division applied).")

    # FOUR: Convert income to numeric and clean impossible values
    final_data["median_income"] = pd.to_numeric(
        final_data.get("median_income"), errors="coerce"
    )

    # replace non-positive incomes with "NaN" (because these are likely codes/suppressions)
    final_data.loc[final_data["median_income"] <= 0, "median_income"] = pd.NA

    # FIVE: quick check
    print("\nAfter cleaning:")
    print(
        final_data[["zip_code", "mean_commute_time", "median_income"]]
        .head(10)
        .to_string(index=False)
    )

    print("\nmean_commute_time describe:")
    print(final_data["mean_commute_time"].describe())

    print("\nmedian_income describe:")
    print(final_data["median_income"].describe())

    print("\nMissing values:")
    print(final_data[["mean_commute_time", "median_income"]].isna().sum())

    # SIX: Save cleaned dataset
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final_data.to_csv(output_path, index=False)
    print(f"\nSaved cleaned dataset to {output_path}")

    return final_data


def descriptive_analysis(final_data: pd.DataFrame) -> None:
    """
    Run descriptive stats and basic rankings.
    Prints summaries and returns nothing.
    """

    print("\n===== SUMMARY STATISTICS =====")
    print(
        final_data[["mean_commute_time", "median_income", "station_count"]]
        .describe()
        .to_string()
    )

    # Sort ZIP codes by highest mean commute time
    print("\n===== TOP 10 ZIPS BY MEAN COMMUTE TIME (raw) =====")
    print(
        final_data.sort_values(by="mean_commute_time", ascending=False)[
            ["zip_code", "mean_commute_time", "median_income"]
        ]
        .head(10)
        .to_string(index=False)
    )

    # ZIP-level average values
    zip_means = (
        final_data.groupby("zip_code")[["mean_commute_time", "median_income"]]
        .mean()
        .reset_index()
    )

    longest_commutes = zip_means.sort_values(
        by="mean_commute_time", ascending=False
    )

    print("\n===== TOP 10 ZIPS BY MEAN COMMUTE TIME (grouped) =====")
    print(
        longest_commutes[["zip_code", "mean_commute_time", "median_income"]]
        .head(10)
        .to_string(index=False)
    )

    highest_income = zip_means.sort_values(by="median_income", ascending=False)

    print("\n===== TOP 10 ZIPS BY MEDIAN INCOME =====")
    print(
        highest_income[["zip_code", "mean_commute_time", "median_income"]]
        .head(10)
        .to_string(index=False)
    )

    # High commute, high income vs high commute, low income
    top_commute = np.percentile(
        final_data["mean_commute_time"].dropna(), 75
    )
    top_income = np.percentile(
        final_data["median_income"].dropna(), 75
    )
    bottom_income = np.percentile(
        final_data["median_income"].dropna(), 25
    )

    high_commute_high_income = final_data[
        (final_data["mean_commute_time"] >= top_commute)
        & (final_data["median_income"] >= top_income)
    ]

    high_commute_low_income = final_data[
        (final_data["mean_commute_time"] >= top_commute)
        & (final_data["median_income"] <= bottom_income)
    ]

    print(
        "\n===== HIGH COMMUTE & HIGH INCOME (75th percentile both) ====="
    )
    print(
        high_commute_high_income[
            ["zip_code", "mean_commute_time", "median_income"]
        ]
        .to_string(index=False)
    )

    print(
        "\n===== HIGH COMMUTE & LOW INCOME (top commute, bottom income) ====="
    )
    print(
        high_commute_low_income[
            ["zip_code", "mean_commute_time", "median_income"]
        ]
        .to_string(index=False)
    )


def make_plots(final_data: pd.DataFrame) -> None:
    """
    Produce histograms, scatterplots, and correlation heatmaps.
    Shows plots but does not save them to disk.
    """

    # Histogram of commute times
    plt.figure()
    final_data["mean_commute_time"].hist()
    plt.xlabel("Mean Commute Time (minutes)")
    plt.ylabel("Number of ZIP Codes")
    plt.title("Distribution of Commute Times")
    plt.show()

    # Scatterplot: income vs commute
    plt.figure()
    plt.scatter(final_data["median_income"], final_data["mean_commute_time"])
    plt.xlabel("Median Household Income")
    plt.ylabel("Mean Commute Time (minutes)")
    plt.title("Commute Time vs Income")
    plt.show()

    # Correlations
    print("\n===== CORRELATIONS: COMMUTE TIME VS MEDIAN INCOME =====")
    print(
        final_data[["mean_commute_time", "median_income"]]
        .corr()
        .to_string()
    )

    # Prepare ZIP-level stats
    zip_stats = final_data[
        ["zip_code", "mean_commute_time", "median_income", "station_count"]
    ].copy()

    corr_matrix = zip_stats[
        ["mean_commute_time", "median_income", "station_count"]
    ].corr()

    print("\n===== CORRELATION MATRIX (commute, income, stations) =====")
    print(corr_matrix.to_string())

    # Heatmap of correlation matrix
    plt.figure(figsize=(6, 5))
    sns.heatmap(corr_matrix, annot=True, cmap="Reds", square=True)
    plt.title("Correlation Matrix: Commute, Income, Station Count")
    plt.show()

    # Commute time in ZIPs with vs. without a station
    zip_stats["has_station"] = zip_stats["station_count"] > 0
    group_means = zip_stats.groupby("has_station")["mean_commute_time"].mean()
    print("\n===== MEAN COMMUTE TIME BY HAS_STATION =====")
    print(group_means.to_string())

    # Binary correlation heatmap
    binary_corr = zip_stats[["mean_commute_time", "has_station"]].corr()
    plt.figure(figsize=(4, 4))
    sns.heatmap(binary_corr, annot=True, cmap="Reds", square=True)
    plt.title("Correlation: Commute Time vs Has Station")
    plt.show()

    # Scatter: station count vs commute
    plt.figure(figsize=(8, 6))
    plt.scatter(zip_stats["station_count"], zip_stats["mean_commute_time"])
    plt.xlabel("Number of Metro Stations in ZIP")
    plt.ylabel("Mean Commute Time (minutes)")
    plt.title("Commute Time vs Station Density")
    plt.show()


def run_regression(clean_data_path: str = FINAL_DATA_CLEAN_CSV) -> None:
    """
    Run OLS regression:
        mean_commute_time ~ median_income + station_count
    using the cleaned dataset.
    """

    df = pd.read_csv(clean_data_path)

    # Drop rows with missing values in key variables
    zip_clean = df.dropna(
        subset=["mean_commute_time", "median_income", "station_count"]
    )

    X = zip_clean[["median_income", "station_count"]]
    X = sm.add_constant(X)
    y = zip_clean["mean_commute_time"]

    model = sm.OLS(y, X).fit()
    print("\n===== OLS REGRESSION RESULTS =====")
    print(model.summary())


if __name__ == "__main__":
    print("Running final_analysis.py...")

    # 1. Load and clean, writes FINAL_DATA_CLEAN_CSV
    final_data = load_and_clean_final_data(
        input_path=FINAL_DATA_CSV,
        output_path=FINAL_DATA_CLEAN_CSV,
    )

    # 2. Descriptive stats
    descriptive_analysis(final_data)

    # 3. Plots
    make_plots(final_data)

    # 4. Regression on cleaned file
    run_regression(FINAL_DATA_CLEAN_CSV)
