# tests.py
from commute_times_retrieval import get_la_commute_zips

#can use a sample of ZIP codes to test quickly
test_zips = ["90001", "90002", "90003"]

def test_la_commute_zips():
    #calling the function
    df = get_la_commute_zips(test_zips)
    
    #Checking that the DataFrame has the correct number of rows
    assert df.shape[0] == len(test_zips), "Number of rows does not match number of test ZIPs"
    
    #checking that required columns exist
    expected_columns = ["NAME", "B08303_001E", "state", "zip_code"]
    for col in expected_columns:
        assert col in df.columns, f"Missing column: {col}"
    
    #checking that all test ZIPs are in the zip_code column
    missing_zips = [z for z in test_zips if z not in df["zip_code"].values]
    assert not missing_zips, f"Missing ZIPs in DataFrame: {missing_zips}"
    
    print("Okay: ACS LA ZIP commute data retrieved correctly")

#if this file is executed directly, run the test 
if __name__ == "__main__":
    test_la_commute_zips()

