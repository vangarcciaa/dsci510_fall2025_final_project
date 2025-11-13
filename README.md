# Does Living Near a Metro Station Reduce Commute Time?
This project explores whether areas in Los Angeles with greater access to metro stations have a shorter average commute time, additionally, we will be analyzing median household income for homes closest to the metro stations in Los Angeles. The goal is to test the assumption that proximity to public transit rails resuces travel time for workers in Los Angeles, a historically commuter dense city, additionally we are exploring to see what household incomes are for those around metro stations. 

# Data sources
This project uses geographic data from LA Metro to locate the location of all metro transit stops in Los Angeles County, I will be using their shapefiles to locate transit stop locations. The variables that will be used are: STOP_NAME, STOP_LAT, AND STOP_LON. To get commute time and median household income information, I will be using two different tables from the 5-year American Community Survey API data, and match by zipcode to the location of the LA metro transit stops. 


1. Data by Stations: All Rail Stations Combined - 07/2023. [ZIP, 7 KB]
Description: A single shapefile that contains all stations for all lines. 
Source: https://developer.metro.net/gis-data/
Type: file-download (archive) of shapefiles
Variables: STOP_NAME, STOP_LAT, STOP_LON
Data form: shapefiles
Data size: 7 KB


2. Mean Travel Time to Work (ACS Table B08303, by ZIP Code or County) 
Source: https://www.census.gov/data/developers/data-sets/acs-5year.html
Type: API
Field/Table: B08303_001E – Mean commute time (estimate), NAME – Geography name
Data size: 200–400 ZIP codes in LA County, very small (<1 MB)


3. Median Household Income (ACS Table B19013, by ZIP Code or County)
Source: https://www.census.gov/data/developers/data-sets/acs-5year.html
Type: API
Field/Table: B19013_001E – Median household income (estimate), NAME – Geography name
Data size: 200–400 ZIP codes in LA County, very small (<1 MB)



# Results 
_describe your findings_




# Installation
- _describe what API keys, user must set where (in .enve) to be able to run the project._
- _describe what special python packages you have used_




# Running analysis 
_update these instructions_




From `src/` directory run:

`python main.py `

Results will appear in `results/` folder. All obtained will be stored in `data/`
