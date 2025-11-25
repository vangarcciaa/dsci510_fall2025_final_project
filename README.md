# Does Living Near a Metro Station Reduce Commute Time?
This project explores whether areas in Los Angeles with greater access to metro stations have a shorter average commute time, additionally, we will be analyzing median household income for homes closest to the metro stations in Los Angeles. The goal is to test the assumption that proximity to public transit rails resuces travel time for workers in Los Angeles, a historically commuter dense city. Additionally, I plan to include median household income as a control variable in the regression model to account for socioeconomic factors that may influence commute behavior.


# Data sources
This project uses geographic data from LA Metro to locate the location of all metro transit stops in Los Angeles County, I will be using their shapefiles to locate transit stop locations. The variables that will be used are: STOP_NAME, STOP_LAT, AND STOP_LON. To get commute time and median household income information, I will be using two different tables from the 5-year American Community Survey API data, and match by geography to the location of the LA metro transit stops. 

1. Data by Stations: All Rail Stations Combined - 07/2023. [ZIP, 7 KB]
Description: A single shapefile that contains all stations for all lines. 
Source: https://developer.metro.net/gis-data/
Type: file-download (archive) of shapefiles
Variables: STOP_NAME, STOP_LAT, STOP_LON
Data form: shapefiles
Data size: 7 KB

2. American Community Survey, 2022 (5-Year Estimate)
Variable: Mean Travel Time to Work (ACS Table S0801_C02_001E, by ZIP Code or County) 
Source: https://api.census.gov/data/2022/acs/acs5/subject
Type: API
Field/Table: S0801_C02_001E – Mean commute time (estimate), NAME – Geography name
Data size: 200–400 ZIP codes in LA County, very small (<1 MB)
Variable: Median Household Income (ACS Table B19013, by ZIP Code or County)
Source: https://www.census.gov/data/developers/data-sets/acs-5year.html
Type: API
Field/Table: B19013_001E – Median household income (estimate), NAME – Geography name
Data size: 200–400 ZIP codes in LA County, very small (<1 MB)


3. US Census Bureau - ZCTA-to-County Crosswalk
Description:  United States Census Bureau map data with zip code information. 
Source: https://www2.census.gov/geo/docs/maps-data/data/rel/zcta_county_rel_10.txt
Type: txt file
Variables: ZCTA5,STATE,COUNTY,GEOID,POPPT,HUPT,AREAPT,AREALANDPT,ZPOP,ZHU,ZAREA,ZAREALAND,COPOP,COHU,
COAREA,COAREALAND,ZPOPPCT,ZHUPCT,ZAREAPCT,ZAREALANDPCT,COPOPPCT,COHUPCT,COAREAPCT,COAREALANDPC
Data form: text file
Data size: 6.3M 


4. US Census Bureau TIGER/Line 2020 Shapefiles
Description:  Census TIGER shapefile: tl_2020_us_zcta520.shp 
Source: https://www2.census.gov/geo/tiger/TIGER2020/ZCTA520/
Type: file-download of shapefile
Variables: ZCTA5CE20, GEOID20, ALAND20, AWATER20, INTPTLAT20, INTPTLON20, FUNCSTAT20, MTFCC20, CLASSFP20
Data form: shapefile
Data size: 819.2 MB



# Results 
_describe your findings_

Key Findings: 
Income is strongly related to commute time. 
Station count has no meaningful effect. 
Overall Model Fit:
- R-squared is 0.09 > the model explains about 9% of ZIP-level commute time differences, which is typical for neighborhood-level social data
- The significant part of the model is income. 
- Station count adds no explanatory power
After controlling for income, the presences of Metro station does not meaningfully reduces commute times. Wealthier ZIP codes constantly show shorter commutes, suggesting that socioeconomic factors-not station-proximity- are driving the commute time differences. 



# Installation
- _describe what API keys, user must set where (in .enve) to be able to run the project._
You'll need a Census API key to run this project. 
It should be the first row and the only content within the .env file
Add it to a .env file in the project folder like this: 
CENSUS_API_KEY=your_key_here

- _describe what special python packages you have used_
The packages you'll need are (also located in the 'requirements.txt') file: 
requests (to call the ACS API)
os
time
numpy
pandas
seaborn
requests
geopandas
python-dotenv
statsmodels.api
matplotlib.pyplot
from io import BytesIO
from dotenv import load_dotenv


Instructions: 
- The .env file contains the API Key (you will need to create, see instructions above)
- 'main.py' runs the full ZIP-level retrieval and saves the CSV.
- 'tests.py' checks if the function is running correctly


# Running analysis 
_update these instructions_
IN-PROGRESS. (NEED TO UPDATE FOR FINAL SUBMISSION).


##### FOR THE PROGRESS REPORT #######
From `src/` directory run:

`python main.py `

The ZIP-level commute data will appear in `data/` folder as 'la_county_commute_zips.csv'.
Results of the analysis will be save in the 'results/' folder.
