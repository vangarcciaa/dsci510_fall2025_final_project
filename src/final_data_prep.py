import os
import requests
import pandas as pd
from io import BytesIO
import geopandas as gpd


def get_la_zip_frame():
    """
    Returns a DataFrame with one row per LA County ZIP code (zip_code column).
    """
    url = "https://www2.census.gov/geo/docs/maps-data/data/rel/zcta_county_rel_10.txt"
    response = requests.get(url)

    # check
    if response.status_code != 200:
        raise RuntimeError(f"Failed to download crosswalk: {response.status_code}")

    # ran into an error initally so I'm telling pandas it's a comma-separated file
    crosswalk = pd.read_csv(BytesIO(response.content), dtype=str, sep=",")

    la_county_zips = crosswalk[
        (crosswalk["STATE"] == "06") & (crosswalk["COUNTY"] == "037")
    ]["ZCTA5"].unique()

    zip_full = pd.DataFrame({"zip_code": la_county_zips})
    zip_full["zip_code"] = zip_full["zip_code"].astype(str)
    return zip_full



def build_final_dataset(
    commute_csv: str,
    income_csv: str,
    stations_shp: str,
    zcta_shp: str,
) -> pd.DataFrame:
    """
    Build final ZIP-level dataset with:
    - zip_code
    - station_count
    - mean_commute_time
    - median_income
    """
    zip_full = get_la_zip_frame()

    # load Metro stations and ZCTA polygons
    stations = gpd.read_file(stations_shp)
    zcta = gpd.read_file(zcta_shp)

    stations = stations.to_crs(zcta.crs)

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

    station_counts = (
        stations_with_zips.groupby("zip_code")["STOP_ID"]
        .count()
        .reset_index(name="station_count")
    )

    zip_full = zip_full.merge(station_counts, on="zip_code", how="left")
    zip_full["station_count"] = zip_full["station_count"].fillna(0)

    # load ACS data
    commute_data = pd.read_csv(commute_csv)
    income_data = pd.read_csv(income_csv)

    commute_data["zip_code"] = commute_data["zip_code"].astype(str)
    income_data["zip_code"] = income_data["zip_code"].astype(str)

    final_data = (
        zip_full
        .merge(
            commute_data[["zip_code", "mean_commute_minutes"]],
            on="zip_code", how="left"
        )
        .merge(
            income_data[["zip_code", "median_household_income"]],
            on="zip_code", how="left"
        )
    )

    final_data = final_data.rename(
        columns={
            "mean_commute_minutes": "mean_commute_time",
            "median_household_income": "median_income",
        }
    )
    return final_data


if __name__ == "__main__":
    df = build_final_dataset(
        commute_csv="data/la_county_commute_zips.csv",
        income_csv="data/la_county_income_zips.csv",
        stations_shp="230711_All_MetroRail_Stations.shp",
        zcta_shp="tl_2020_us_zcta520.shp",
    )
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/final_data.csv", index=False)




















