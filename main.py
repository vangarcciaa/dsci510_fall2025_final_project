# src/main.py
#purpose of this file is so that it's easier to run the function

from commute_times_retrieval import get_la_commute_zips
import os
import pandas as pd

#defining small sample of my list of LA County ZIP codes
la_zips = ["90001", "90002", "90003", "90004", "90005"] 

#retrieving commute times using my function
df_zips = get_la_commute_zips(la_zips)

#making sure the data folder exists
os.makedirs("data", exist_ok=True)

#saving results to CSV
output_file = "data/la_county_commute_zips.csv"
df_zips.to_csv(output_file, index=False)

print(f"ZIP-level commute data saved to {output_file}")
