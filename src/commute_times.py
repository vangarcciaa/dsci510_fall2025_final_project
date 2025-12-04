# importing the packages
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


def get_la_commute_zips(la_zips):
    """
    Pull mean commute time for a list of LA County ZIP codes.
    """
    url = "https://api.census.gov/data/2022/acs/acs5/subject"
    results = []

    for z in la_zips:
        params = {
            "get": "NAME,S0801_C02_001E",
            "for": f"zip code tabulation area:{z}",
            "key": API_KEY
        }
        r = requests.get(url, params=params)
        if r.status_code == 200:
            data = r.json()
            if len(data) > 1:
                results.append([data[1][0], data[1][1], z])
            else:
                results.append([f"ZCTA5 {z}", None, z])
        else:
            results.append([f"ZCTA5 {z}", None, z])
        time.sleep(0.2)

    df = pd.DataFrame(results, columns=["NAME", "mean_commute_minutes", "zip_code"])
    df["mean_commute_minutes"] = pd.to_numeric(df["mean_commute_minutes"], errors="coerce")

    # convert ACS scaled integer field
    # when I first looked at the figure the numbers were extremely high, after reviewing it seems like it was converted when I first downloaed it. 
    df["mean_commute_minutes"] = df["mean_commute_minutes"] / 1000  
    return df


if __name__ == "__main__":
    print("running commute_times.py")
    la_zips = get_la_county_zips()
    df_commute = get_la_commute_zips(la_zips)

    os.makedirs("data", exist_ok=True)
    df_commute.to_csv("data/la_county_commute_zips.csv", index=False)

    print("saved ZIP-level commute data to data/la_county_commute_zips.csv")
    print(df_commute.head())



