pip install geopandas
import geopandas as gpd
import pandas as pd

#????? DO I INCLUDE THIS HERE ??????
#path to the shapefile
shp_path = "230711_All_MetroRail_Stations.shp"
gdf = gpd.read_file(shp_path)

#checking to see if it was successful 
print(gdf.head())
print(gdf.columns)

#converting to pandas DataFrame
df = pd.DataFrame(gdf.drop(columns="geometry"))
print(df.head())

#this file comes with latitude and longitude data
#using geometry function to store each station location as a point (longitude, latitude)
#(LAT,LONG) is the format for GIS shapefiles
gdf["lon"] = gdf.geometry.x
gdf["lat"] = gdf.geometry.y

#saving to csv file 
gdf.to_csv("metro_stations.csv", index=False)
