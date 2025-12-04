import os
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import matplotlib.pyplot as plt


def clean_final_data(input_csv: str, output_csv: str) -> pd.DataFrame:
    final_data = pd.read_csv(input_csv)

    # final clean up 
    if "NAME_x" in final_data.columns and "NAME_y" in final_data.columns:
        final_data = final_data.drop(columns=["NAME_x"])
        final_data = final_data.rename(columns={"NAME_y": "zcta_name"})
    elif "NAME_x" in final_data.columns:
        final_data = final_data.rename(columns={"NAME_x": "zcta_name"})
    elif "NAME_y" in final_data.columns:
        final_data = final_data.rename(columns={"NAME_y": "zcta_name"})

    # commute time
    final_data["mean_commute_time"] = pd.to_numeric(
        final_data["mean_commute_time"], errors="coerce"
    )
    commute_median = final_data["mean_commute_time"].median(skipna=True)
    if pd.notna(commute_median) and commute_median > 100:
        final_data["mean_commute_time"] = final_data["mean_commute_time"] / 1000.0

    # income
    final_data["median_income"] = pd.to_numeric(
        final_data["median_income"], errors="coerce"
    )
    final_data.loc[final_data["median_income"] <= 0, "median_income"] = pd.NA

    os.makedirs("data", exist_ok=True)
    final_data.to_csv(output_csv, index=False)
    return final_data


def run_descriptive_plots(final_data: pd.DataFrame):
    # histogram
    final_data["mean_commute_time"].hist()
    plt.xlabel("Mean Commute Time (minutes)")
    plt.ylabel("Number of ZIP Codes")
    plt.title("Distribution of Commute Times")
    plt.show()

    # scatter plot: income vs commute
    plt.scatter(final_data["median_income"], final_data["mean_commute_time"])
    plt.xlabel("Median Household Income")
    plt.ylabel("Mean Commute Time")
    plt.title("Commute Time vs Income")
    plt.show()

    # correlations
    zip_stats = final_data[["zip_code", "mean_commute_time",
                            "median_income", "station_count"]].copy()
    corr_matrix = zip_stats[["mean_commute_time", "median_income",
                             "station_count"]].corr()
    plt.figure(figsize=(6, 5))
    sns.heatmap(corr_matrix, annot=True, cmap="Reds", square=True)
    plt.title("Correlation Matrix")
    plt.show()

    # has_station vs commute
    zip_stats["has_station"] = zip_stats["station_count"] > 0
    binary_corr = zip_stats[["mean_commute_time", "has_station"]].corr()
    sns.heatmap(binary_corr, annot=True, cmap="Reds", square=True)
    plt.title("Commute vs Has Station")
    plt.show()

    # scatter plot station_count vs commute
    plt.figure(figsize=(8, 6))
    plt.scatter(zip_stats["station_count"], zip_stats["mean_commute_time"])
    plt.xlabel("Number of Metro Stations in ZIP")
    plt.ylabel("Mean Commute Time (minutes)")
    plt.title("Commute Time vs Station Density")
    plt.show()


def run_regression(final_data: pd.DataFrame):
    zip_clean = final_data.dropna(
        subset=["mean_commute_time", "median_income", "station_count"]
    )

    X = zip_clean[["median_income", "station_count"]]
    X = sm.add_constant(X)
    y = zip_clean["mean_commute_time"]

    model = sm.OLS(y, X).fit()
    print(model.summary())
    return model


if __name__ == "__main__":
    df = clean_final_data("data/final_data.csv", "data/final_data_cleaned.csv")
    run_descriptive_plots(df)
    run_regression(df)
