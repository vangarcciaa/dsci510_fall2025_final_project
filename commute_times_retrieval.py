#Created the '.env' file from this cell using this code: 

#with open(".env", "w") as f:
#f.write("CENSUS_API_KEY=my_key\n")

!pip install requests pandas python-dotenv

#check

import requests, pandas, dotenv, os
print("All packages imported successfully")


#create the necessary folders and files

for folder in ["data", "results", "src"]:
    os.makedirs(folder, exist_ok=True)

print("Folders created successfully.")

#creating a 'gitignore' file so Git will ignore

with open(".gitignore", "w") as f:
    f.write(".env\n")
    f.write("data/\n")
    f.write("results/\n")


#verifying the existence of the .env and .gitignore files
!ls -a

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

# Convert JSON to DataFrame
data = response.json()
df = pd.DataFrame(data[1:], columns=data[0])

# Show the data
display(df)



#now that I know it works, I am going to do it for zip codes in LA County 
#this list may not be exhaustive, but I'll modify it as I explore the LA transit data

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

import requests
import pandas as pd
from dotenv import load_dotenv
import os
import time  #to add a small delay between requests

#loading API key
load_dotenv()
API_KEY = os.getenv("CENSUS_API_KEY")

#ACS endpoint
url = "https://api.census.gov/data/2022/acs/acs5"

#storing results here
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
            #pad the row with None if columns are missing
            while len(row) < 4:
                row.append(None)
            results.append(row)
        except Exception as e:
            print(f"JSON decode error for ZIP {z}: {e}")
    else:
        print(f"Error for ZIP {z}: {response.status_code}")
    
    time.sleep(0.2)  #small delay to avoid hitting API rate limits

#convert results to DataFrame
df_zips = pd.DataFrame(results, columns=["NAME", "B08303_001E", "state", "zip_code"])
display(df_zips.head())


#show rows where commute time exists
df_zips[df_zips["B08303_001E"].notna()]

#count how many ZIPs have data
print("ZIPs with commute data:", df_zips["B08303_001E"].notna().sum())


#save to CSV

os.makedirs("data", exist_ok=True)
df_zips.to_csv("data/la_county_commute_zips.csv", index=False)
print("Saved ZIP-level commute data to data/la_county_commute_zips.csv")
