import os
import time
import requests
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv

# load API key
load_dotenv()
API_KEY = os.getenv("CENSUS_API_KEY")


def get_la_county_zips():
    """
    Download ZCTA-to-county crosswalk and return a list of LA County ZIP codes.
    """
    url = "https://www2.census.gov/geo/docs/maps-data/data/rel/zcta_county_rel_10.txt"
    response = requests.get(url)
    zcta_crosswalk = pd.read_csv(BytesIO(response.content), dtype=str)

    la_county_zips = zcta_crosswalk[
        (zcta_crosswalk["STATE"] == "06") & (zcta_crosswalk["COUNTY"] == "037")
    ]["ZCTA5"].unique().tolist()
    return la_county_zips


def get_la_income_zips(la_zips):
    """
    Pull median household income (B19013_001E) for a list of LA County ZIP codes.
    Returns a DataFrame with columns: NAME, median_household_income, zip_code
    """
    url = "https://api.census.gov/data/2022/acs/acs5"
    results = []

    for z in la_zips:
        params = {
            "get": "NAME,B19013_001E",
            "for": f"zip code tabulation area:{z}",
            "key": API_KEY
        }

        r = requests.get(url, params=params)
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

        time.sleep(0.2)

    df = pd.DataFrame(results,
                      columns=["NAME", "median_household_income", "zip_code"])
    df["median_household_income"] = pd.to_numeric(
        df["median_household_income"], errors="coerce"
    )
    return df


if __name__ == "__main__":
    print("Running median_hhincome.py")
    la_zips = get_la_county_zips()
    df_income = get_la_income_zips(la_zips)

    os.makedirs("data", exist_ok=True)
    df_income.to_csv("data/la_county_income_zips.csv", index=False)
    print("Saved ZIP-level income data to data/la_county_income_zips.csv")
    print(df_income.head())





