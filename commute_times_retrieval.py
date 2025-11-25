#The first part of this was to test if I could pull the infomation, so I started small and pulled commute time only for LA County 

#importing the packages
import os
import time
import requests
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv


###################### TEST ######################
#retrieving my API key from my .env file
load_dotenv()
API_KEY = os.getenv("CENSUS_API_KEY")

#pulling for LA County, CA to make sure I am able to pull the data
url = "https://api.census.gov/data/2022/acs/acs5"
params = {
    "get": "NAME,B08303_001E",
    "for": "county:037",  
    "in": "state:06",     
    "key": API_KEY
}

#returns the commute time in minutes? need to check this.
response = requests.get(url, params=params)
print("Status code:", response.status_code)
print("Response text:", response.text) 

#convert JSON to DataFrame
data = response.json()
df = pd.DataFrame(data[1:], columns=data[0])

# Show the data
display(df)
##################################################

# load API key
load_dotenv()
API_KEY = os.getenv("CENSUS_API_KEY")

# downloading the ZCTA-to-county crosswalk CSV
# this file maps every ZCTA to counties
url = "https://www2.census.gov/geo/docs/maps-data/data/rel/zcta_county_rel_10.txt"
response = requests.get(url)

# load into a DataFrame
zcta_crosswalk = pd.read_csv(BytesIO(response.content), dtype=str)

# filtering down to LA County (state=06, county=037)
la_county_zips = zcta_crosswalk[
    (zcta_crosswalk["STATE"] == "06") & (zcta_crosswalk["COUNTY"] == "037")
]["ZCTA5"].unique().tolist()

print(f"Total LA County ZIP codes: {len(la_county_zips)}")
print(la_county_zips[:20])  # show first 20 ZIPs


# load API key
load_dotenv()
API_KEY = os.getenv("CENSUS_API_KEY")

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
    df["mean_commute_minutes"] = df["mean_commute_minutes"] / 1000  # convert to minutes
    return df

# pull the data
df_commute = get_la_commute_zips(la_county_zips)

# check results
print("ZIPs with commute data:", df_commute["mean_commute_minutes"].notna().sum())
print(df_commute.describe())


#the commute time numbers are looking very large and after investigating it seems the numbers were scaled up by 1000
#I think this happened when they were changed to numeric format
#this is the assumption because the values as they are now fall between 1,000 and 44,000 
#if we divide by 1,000 it gives more realistic commute times
#ACS numerican fields are returned as integers scaled to avoid decimals during transport - this is common with means and rates

# inspect first few rows
df_commute.head()

# inspect first few rows
df_commute.head()

# checking the first few rows and then all columns and types
df_commute.info()

# save to CSV
os.makedirs("data", exist_ok=True)
df_commute.to_csv("data/la_county_commute_zips.csv", index=False)
print("Saved ZIP-level commute data to data/la_county_commute_zips.csv")
