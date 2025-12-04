from src.commute_times import get_la_county_zips
from src.median_hhincome import get_la_income_zips
from src.metro_station import load_metro_stations
import os


def test_zip_loader():
    zips = get_la_county_zips()

    if not zips:
        print("FAILED: get_la_county_zips() returned an empty list.")
    else:
        print("PASSED: Loaded", len(zips), "ZIP codes.")


def test_income_loader():
    print("Running test_income_loader...")
    zips = get_la_county_zips()
    income_df = get_la_income_zips(zips)

    if income_df is None or income_df.empty:
        print("FAILED: get_la_income_zips() returned empty data.")
    else:
        print("PASSED: Income data loaded with", len(income_df), "rows.")


def test_metro_shapefile():
    print("Running test_metro_shapefile...")

    shp_path = "230711_All_MetroRail_Stations.shp"

    if not os.path.exists(shp_path):
        print(f"SKIPPED: Shapefile not found at {shp_path}.")
        return

    gdf = load_metro_stations(shp_path)

    if gdf is None or gdf.empty:
        print("FAILED: load_metro_stations() returned no data.")
    else:
        print("PASSED: Loaded", len(gdf), "stations.")


if __name__ == "__main__":
    print("\n=== Tests ===\n")
    test_zip_loader()
    test_income_loader()
    test_metro_shapefile()
    print("\n=== Tests Completed ===\n")
