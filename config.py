"""
Configuration file for DSCI510 Final Project.
Contains ONLY constants such as file names, paths, and API URLs.
No API keys should ever be placed here.
"""

# ---------------------------
# File paths
# ---------------------------

# Raw ACS output CSVs
COMMUTE_CSV = "data/la_county_commute_zips.csv"
INCOME_CSV = "data/la_county_income_zips.csv"

# Final merged dataset
FINAL_DATA_CSV = "data/final_data.csv"
FINAL_DATA_CLEAN_CSV = "data/final_data_cleaned.csv"

# Metro shapefile
METRO_STATIONS_SHP = "data/230711_All_MetroRail_Stations.shp"

# ZCTA shapefile
ZCTA_SHP = "data/tl_2020_us_zcta520.shp"

# ---------------------------
# API URLs
# ---------------------------

# Census crosswalk file (ZCTA → County)
ZCTA_CROSSWALK_URL = (
    "https://www2.census.gov/geo/docs/maps-data/data/rel/zcta_county_rel_10.txt"
)

# ACS API URLs
ACS_COMMUTE_URL = "https://api.census.gov/data/2022/acs/acs5/subject"
ACS_INCOME_URL = "https://api.census.gov/data/2022/acs/acs5"

# ---------------------------
# Settings
# ---------------------------

API_SLEEP_SECONDS = 0.2
