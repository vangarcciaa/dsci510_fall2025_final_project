import geopandas as gpd
import pandas as pd
from pathlib import Path


def load_metro_stations(shp_path: str) -> gpd.GeoDataFrame:
    """
    Load LA Metro rail stations shapefile and add lon/lat columns.
    """
    gdf = gpd.read_file(shp_path)
    gdf["lon"] = gdf.geometry.x
    gdf["lat"] = gdf.geometry.y
    return gdf


def save_metro_stations_csv(gdf: gpd.GeoDataFrame,
                            csv_path: str = "metro_stations.csv") -> None:
    """
    Save the stations GeoDataFrame (with lon/lat) to a CSV.
    Keeps the filename the same as before by default.
    """
    Path(csv_path).parent.mkdir(parents=True, exist_ok=True)
    gdf.to_csv(csv_path, index=False)


if __name__ == "__main__":
    shp_path = "230711_All_MetroRail_Stations.shp"
    gdf = load_metro_stations(shp_path)

    print(gdf.head())
    print(gdf.columns)

    df = pd.DataFrame(gdf.drop(columns="geometry"))
    print(df.head())

    save_metro_stations_csv(gdf, "metro_stations.csv")
