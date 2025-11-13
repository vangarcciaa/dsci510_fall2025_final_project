#The first part of this was to test if I could pull the infomation, so I started small and pulled commute time only for LA County 

#importing the packages
import requests
import pandas as pd
from dotenv import load_dotenv
import os


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



import pandas as pd

#convert JSON to DataFrame
data = response.json()
df = pd.DataFrame(data[1:], columns=data[0])

# Show the data
display(df)


#now that I know it works, I am going to do it for zip codes in LA County 
#this list may not be exhaustive, but I'll modify it as I explore the LA transit data file

la_zips = [
    "90001","90002","90003","90004","90005","90006","90007","90008","90010",
    "90011","90012","90013","90014","90015","90016","90017","90018","90019",
    "90020","90021","90022","90023","90024","90025","90026","90027","90028",
    "90029","90031","90032","90033","90034","90035","90036","90037","90038",
    "90039","90040","90041","90042","90043","90044","90045","90046","90047",
    "90048","90049","90056","90057","90058","90059","90061","90062","90063",
    "90064","90065","90066","90067","90068","90069","90071","90077","90089"
]


#pull data for each ZIP using loop function
#importing again so it doesn't create an error

import requests
import pandas as pd
from dotenv import load_dotenv
import os
import time  #to add a small delay between requests

#loading API key from .env
load_dotenv()
API_KEY = os.getenv("CENSUS_API_KEY")

def get_la_commute_zips(la_zips):
    """
    Pull mean commute time (B08303_001E) for a list of LA County ZIP codes.
    
    Parameters:
        la_zips (list): list of ZIP code strings
    
    Returns:
        pd.DataFrame: DataFrame with columns NAME, B08303_001E, state, zip_code
    """
    url = "https://api.census.gov/data/2022/acs/acs5"
    results = []

    for z in la_zips:
        params = {
            "get": "NAME,B08303_001E",
            "for": f"zip code tabulation area:{z}",
            "key": API_KEY
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            try:
                data = response.json()
                row = data[1]
                #pad missing columns if response is shorter than expected
                while len(row) < 4:
                    row.append(None)
                results.append(row)
            except Exception as e:
                print(f"JSON decode error for ZIP {z}: {e}")
                #append a row with None for missing data
                results.append([f"ZCTA5 {z}", None, None, z])
        else:
            print(f"Error for ZIP {z}: {response.status_code}")
            results.append([f"ZCTA5 {z}", None, None, z])
        
        time.sleep(0.2)  #delay to avoid API rate limits
    
    #convert list of results to DataFrame
    df = pd.DataFrame(results, columns=["NAME", "B08303_001E", "state", "zip_code"])
    
    return df


#show rows where commute time exists
df_zips[df_zips["B08303_001E"].notna()]

#count how many ZIPs have data
print("ZIPs with commute data:", df_zips["B08303_001E"].notna().sum())


#save to CSV

os.makedirs("data", exist_ok=True)
df_zips.to_csv("data/la_county_commute_zips.csv", index=False)
print("Saved ZIP-level commute data to data/la_county_commute_zips.csv")
