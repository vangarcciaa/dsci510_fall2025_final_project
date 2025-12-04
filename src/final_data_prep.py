import os
import requests
import pandas as pd
import geopandas as gpd
from io import BytesIO

from config import (
    ZCTA_CROSSWALK_URL,
    COMMUTE_CSV,
    INCOME_CSV,
    FINAL_DATA_CSV,
    METRO_STATIONS_SHP,
    ZCTA_SHP,
)


def get_la_zip_frame() -> pd.DataFrame:
    """
    Download the ZCTA-to-county crosswalk and return a DataFrame
    with one row per Los Angeles County ZIP code (zip_code column).
    """
    response = requests.get(ZCTA_CROSSWALK_URL)

    if response.status_code != 200:
        raise RuntimeError(
            f"Failed to download crosswalk file: {response.status_code}"
        )

    crosswalk = pd.read_csv(BytesIO(response.content), dtype=str, sep=",")

    la_county_zips = (
        crosswalk[
            (crosswalk["STATE"] == "06") & (crosswalk["COUNTY"] == "037")
        ]["ZCTA5"]
        .unique()
    )

    zip_full = pd.DataFrame({"zip_code": la_county_zips})
    zip_full["zip_code"] = zip_full["zip_code"].astype(str)

    return zip_full


def build_final_dataset(
    commute_csv: str = COMMUTE_CSV,
    income_csv: str = INCOME_CSV,
    stations_shp: str = METRO_STATIONS_SHP,
    zcta_shp: str = ZCTA_SHP,
) -> pd.DataFrame:
    """
    Build final ZIP-level dataset with:
      - zip_code
      - station_count
      - mean_commute_time
      - median_income
    """

    # Base frame of all LA County ZIPs
    zip_full = get_la_zip_frame()

    # Loading Geo data 
    stations = gpd.read_file(stations_shp)
    zcta = gpd.read_file(zcta_shp)

    # making sure there is a CRS matches
    stations = stations.to_crs(zcta.crs)

    # Spatial join: assign ZIP (ZCTA5CE20) to each station
    stations_with_zips = gpd.sjoin(
        stations,
        zcta,
        how="left",
        predicate="within",
    )

    stations_with_zips = stations_with_zips.rename(
        columns={"ZCTA5CE20": "zip_code"}
    )
    stations_with_zips["zip_code"] = stations_with_zips["zip_code"].astype(str)

    # Count stations per ZIP
    station_counts = (
        stations_with_zips.groupby("zip_code")["STOP_ID"]
        .count()
        .reset_index(name="station_count")
    )

    # Merge onto the complete ZIP list
    zip_full = zip_full.merge(station_counts, on="zip_code", how="left")
    zip_full["station_count"] = zip_full["station_count"].fillna(0)

    # ---- Load ACS commute & income CSVs ----
    commute_data = pd.read_csv(commute_csv)
    income_data = pd.read_csv(income_csv)

    commute_data["zip_code"] = commute_data["zip_code"].astype(str)
    income_data["zip_code"] = income_data["zip_code"].astype(str)

    # Merge all data into one ZIP-level DataFrame
    final_data = (
        zip_full.merge(
            commute_data[["zip_code", "mean_commute_minutes"]],
            on="zip_code",
            how="left",
        )
        .merge(
            income_data[["zip_code", "median_household_income"]],
            on="zip_code",
            how="left",
        )
    )

    # Rename columns for consistency
    final_data = final_data.rename(
        columns={
            "mean_commute_minutes": "mean_commute_time",
            "median_household_income": "median_income",
        }
    )

    return final_data


if __name__ == "__main__":
    
    final_data = build_final_dataset()

    os.makedirs("data", exist_ok=True)
    final_data.to_csv(FINAL_DATA_CSV, index=False)

    print(f"Saved ZIP-level dataset to {FINAL_DATA_CSV}")
    print(final_data.head())



















