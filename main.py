"""
main.py
Run the full project from start to finish.
"""

import os

from src.commute_times import get_la_county_zips, get_la_commute_zips
from src.median_hhincome import get_la_income_zips
from src.final_data_prep import build_final_dataset
from src.final_analysis import run_all_analysis

from config import (
    DATA_DIR,
    COMMUTE_CSV,
    INCOME_CSV,
    FINAL_DATA_CSV,
    METRO_STATIONS_SHP,
    ZCTA_SHP,
)

def main():

    print("\n=== START ===\n")

    # --------------------------
    # ONE: Load LA ZIP codes
    # --------------------------
    print("\nLoading LA County ZIP codes")
    la_zips = get_la_county_zips()
    print(f"Loaded {len(la_zips)} ZIP codes.")

    # ------------------------------------------------
    # TWO: Retrieve commute time data from the ACS
    # ------------------------------------------------
    print("\nPull commute time data from ACS")
    commute_df = get_la_commute_zips(la_zips)
    os.makedirs(DATA_DIR, exist_ok=True)
    commute_df.to_csv(COMMUTE_CSV, index=False)
    print(f"Saved commute data → {COMMUTE_CSV}")

    # ----------------------------------------------------
    # THREE: Retrieve median household income from ACS
    # ----------------------------------------------------
    print("\nPull median household income from ACS")
    income_df = get_la_income_zips(la_zips)
    income_df.to_csv(INCOME_CSV, index=False)
    print(f"Saved income data → {INCOME_CSV}")

    # ---------------------------------------------------------
    # FOUR: Build final merged ZIP-level dataset
    # ---------------------------------------------------------
    print("\nBuild final merged dataset")
    final_df = build_final_dataset(
        commute_csv=COMMUTE_CSV,
        income_csv=INCOME_CSV,
        stations_shp=METRO_STATIONS_SHP,
        zcta_shp=ZCTA_SHP,
    )
    final_df.to_csv(FINAL_DATA_CSV, index=False)
    print(f"Saved final merged dataset → {FINAL_DATA_CSV}")

    # -----------------------------------------------
    # FIVE: Run descriptive + regression analysis
    # -----------------------------------------------
    print("\nRun analysis")
    run_all_analysis(FINAL_DATA_CSV)

    print("\n=== DONE ===\n")


if __name__ == "__main__":
    main()
