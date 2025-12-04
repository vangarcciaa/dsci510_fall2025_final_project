import os
import time
import requests
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv

from config import (
    ZCTA_CROSSWALK_URL,
    ACS_INCOME_URL,
    INCOME_CSV,
    API_SLEEP_SECONDS,
)

# Load API key from .env 
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
            (zcta_crosswalk["STATE"] == "06")   # CA
            & (zcta_crosswalk["COUNTY"] == "037")  # LA County
        ]["ZCTA5"]
        .unique()
        .tolist()
    )
    return la_zips


def get_la_income_zips(la_zips):
    """
    Pull median household income (B19013_001E) for list of LA County ZIP codes.

    Return a DataFrame with columns:
    - NAME
    - median_household_income
    - zip_code
    """
    results = []

    for z in la_zips:
        params = {
            "get": "NAME,B19013_001E",
            "for": f"zip code tabulation area:{z}",
            "key": API_KEY,
        }

        r = requests.get(ACS_INCOME_URL, params=params)

        if r.status_code == 200:
            try:
                data = r.json()
                if len(data) > 1:
                    name = data[1][0]
                    income = data[1][1]
                    results.append([name, income, z])
                else:
                    results.append([f"ZCTA5 {z}", None, z])
            except Exception as e:
                print(f"JSON decode error for ZIP {z}: {e}")
                results.append([f"ZCTA5 {z}", None, z])
        else:
            print(f"Error for ZIP {z}: {r.status_code}")
            results.append([f"ZCTA5 {z}", None, z])

        time.sleep(API_SLEEP_SECONDS)

    df = pd.DataFrame(
        results, columns=["NAME", "median_household_income", "zip_code"]
    )
    df["median_household_income"] = pd.to_numeric(
        df["median_household_income"], errors="coerce"
    )
    return df


if __name__ == "__main__":
    print("Running median_hhincome.py...")

    la_zips = get_la_county_zips()
    df_income = get_la_income_zips(la_zips)

    os.makedirs("data", exist_ok=True)
    df_income.to_csv(INCOME_CSV, index=False)

    print(f"Saved income data to {INCOME_CSV}")





