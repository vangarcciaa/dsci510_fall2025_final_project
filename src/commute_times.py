import os
import time
import requests
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv

# import constants from config.py
from config import (
    ZCTA_CROSSWALK_URL,
    ACS_COMMUTE_URL,
    COMMUTE_CSV,
    API_SLEEP_SECONDS,
)

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("CENSUS_API_KEY")


def get_la_county_zips():
    """
    Download ZCTA-to-county crosswalk and return a list of LA County ZIP codes.
    """
    response = requests.get(ZCTA_CROSSWALK_URL)
    zcta_crosswalk = pd.read_csv(BytesIO(response.content), dtype=str, sep=",")

    la_zips = (
        zcta_crosswalk[
            (zcta_crosswalk["STATE"] == "06") & (zcta_crosswalk["COUNTY"] == "037")
        ]["ZCTA5"]
        .unique()
        .tolist()
    )
    return la_zips


def get_la_commute_zips(la_zips):
    """
    Pull mean commute time for a list of LA County ZIP codes.
    Return DataFrame with columns NAME, mean_commute_minutes, zip_code.
    """
    results = []

    for z in la_zips:
        params = {
            "get": "NAME,S0801_C02_001E",
            "for": f"zip code tabulation area:{z}",
            "key": API_KEY,
        }

        r = requests.get(ACS_COMMUTE_URL, params=params)

        if r.status_code == 200:
            data = r.json()
            if len(data) > 1:
                results.append([data[1][0], data[1][1], z])
            else:
                results.append([f"ZCTA5 {z}", None, z])
        else:
            print(f"Error for ZIP {z}: {r.status_code}")
            results.append([f"ZCTA5 {z}", None, z])

        time.sleep(API_SLEEP_SECONDS)

    df = pd.DataFrame(results, columns=["NAME", "mean_commute_minutes", "zip_code"])

    # Convert commute time from scaled integer (ACS format) to minutes
    df["mean_commute_minutes"] = pd.to_numeric(
        df["mean_commute_minutes"], errors="coerce"
    )
    df["mean_commute_minutes"] = df["mean_commute_minutes"] / 1000.0

    return df


if __name__ == "__main__":
    print("Running commute_times.py")

    la_zips = get_la_county_zips()
    df_commute = get_la_commute_zips(la_zips)

    os.makedirs("data", exist_ok=True)
    df_commute.to_csv(COMMUTE_CSV, index=False)

    print(f"Saved commute data to {COMMUTE_CSV}")
