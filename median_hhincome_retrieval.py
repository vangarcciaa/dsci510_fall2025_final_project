# Pull Median Household Income for LA Zip Codes


import requests
import pandas as pd
from dotenv import load_dotenv
import os
import time

# Load API key
load_dotenv()
API_KEY = os.getenv("CENSUS_API_KEY")

def get_la_income_zips(la_zips):
    """
    Pull median household income (B19013_001E) for a list of LA County ZIP codes.
    
    Parameters:
        la_zips (list): list of ZIP code strings
    
    Returns:
        pd.DataFrame: DataFrame with columns NAME, B19013_001E, state, zip_code
    """
    url = "https://api.census.gov/data/2022/acs/acs5"
    results = []

    for z in la_zips:
        params = {
            "get": "NAME,B19013_001E",
            "for": f"zip code tabulation area:{z}",
            "key": API_KEY
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            try:
                data = response.json()
                row = data[1]
                # pad missing columns if needed
                while len(row) < 4:
                    row.append(None)
                results.append(row)
            except Exception as e:
                print(f"JSON decode error for ZIP {z}: {e}")
                results.append([f"ZCTA5 {z}", None, None, z])
        else:
            print(f"Error for ZIP {z}: {response.status_code}")
            results.append([f"ZCTA5 {z}", None, None, z])
        
        time.sleep(0.2)  # avoids API rate limits
    
    df = pd.DataFrame(results, columns=["NAME", "B19013_001E", "state", "zip_code"])
    return df

# Run the function and inspect results 

la_zips = [
    "90001","90002","90003","90004","90005","90006","90007","90008","90010",
    "90011","90012","90013","90014","90015","90016","90017","90018","90019",
    "90020","90021","90022","90023","90024","90025","90026","90027","90028",
    "90029","90031","90032","90033","90034","90035","90036","90037","90038",
    "90039","90040","90041","90042","90043","90044","90045","90046","90047",
    "90048","90049","90056","90057","90058","90059","90061","90062","90063",
    "90064","90065","90066","90067","90068","90069","90071","90077","90089"
]


df_income = get_la_income_zips(la_zips)

# Show a few rows
display(df_income.head())

print("ZIPs with income data:", df_income["B19013_001E"].notna().sum())


# Save to CSV

os.makedirs("data", exist_ok=True)
df_income.to_csv("data/la_county_income_zips.csv", index=False)
print("Saved ZIP-level income data to data/la_county_income_zips.csv")
