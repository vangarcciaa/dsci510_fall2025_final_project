import os
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import matplotlib.pyplot as plt


# load
final_data = pd.read_csv("data/final_data.csv")

# Clean up NAME cols
if "NAME_x" in final_data.columns and "NAME_y" in final_data.columns:
    final_data = final_data.drop(columns=["NAME_x"])
    final_data = final_data.rename(columns={"NAME_y": "zcta_name"})
elif "NAME_x" in final_data.columns:
    final_data = final_data.rename(columns={"NAME_x": "zcta_name"})
elif "NAME_y" in final_data.columns:
    final_data = final_data.rename(columns={"NAME_y": "zcta_name"})

# Ensure commute column is numeric
final_data["mean_commute_time"] = pd.to_numeric(final_data["mean_commute_time"], errors="coerce")

# Detect whether values are still scaled (raw ACS) and divide by 1000 if needed.
commute_median = final_data["mean_commute_time"].median(skipna=True)
print("median before possible scaling:", commute_median)

if pd.notna(commute_median) and commute_median > 100:
    print("Dividing mean_commute_time by 1000 to convert to minutes...")
    final_data["mean_commute_time"] = final_data["mean_commute_time"] / 1000.0
else:
    print("Values look already in minutes (no division applied).")

# Convert income to numeric and clean impossible values
final_data["median_income"] = pd.to_numeric(final_data["median_income"], errors="coerce")

# replace non-positive incomes with NaN (these are likely codes/suppressions)
final_data.loc[final_data["median_income"] <= 0, "median_income"] = pd.NA

# Quick sanity checks / outputs
print("\nAfter cleaning:")
print(final_data[["zip_code", "mean_commute_time", "median_income"]].head(10))
print("\nmean_commute_time describe:")
print(final_data["mean_commute_time"].describe())
print("\nmedian_income describe:")
print(final_data["median_income"].describe())
print("\nMissing values:")
print(final_data[["mean_commute_time", "median_income"]].isna().sum())

# Save cleaned final_data back to CSV (overwrite or new file)
os.makedirs("data", exist_ok=True)
final_data.to_csv("data/final_data_cleaned.csv", index=False)
print("\nSaved cleaned dataset to data/final_data_cleaned.csv")


#################### SUMMARY STATISTICS ####################

final_data[["mean_commute_time", "median_income", "station_count"]].describe()

#################### HISTOGRAM OF COMMUTE TIMES ####################


import matplotlib.pyplot as plt

final_data["mean_commute_time"].hist()
plt.xlabel("Mean Commute Time (minutes)")
plt.ylabel("Number of ZIP Codes")
plt.title("Distribution of Commute Times")
plt.show()


#################### INCOME VS COMMUTE SCATTERPLOT ####################


plt.scatter(final_data["median_income"], final_data["mean_commute_time"])
plt.xlabel("Median Household Income")
plt.ylabel("Mean Commute Time")
plt.title("Commute Time vs Income")
plt.show()

#################### COMMUTE TIME VS MEDIAN INCOME ####################

# DO WEALTHIER AREAS HAVE SHORTER (OR LONGER) COMMUTES? DO LOWER-INCOME NEIGHBORHOODS EXPERIENCE LONGER COMMUTES

final_data[["mean_commute_time", "median_income"]].corr()

#################### MEDIAN INCOME VS STATION DENSITY (NUMBER OF STATIONS IN ZIP CODE) ####################

# ARE TRANSIT INVESTMENTS EQUITABLY DISTRIBUTED?
import seaborn as sns
import matplotlib.pyplot as plt

# ZIP-level dataset already includes station_count
zip_stats = final_data[["zip_code", "mean_commute_time", "median_income", "station_count"]].copy()

# CORRELATION MATRIX
corr_matrix = zip_stats[["mean_commute_time", "median_income", "station_count"]].corr()
corr_matrix

# HEAT MAP 
plt.figure(figsize=(6,5))
sns.heatmap(corr_matrix, annot=True, cmap="Reds", square=True)
plt.title("Correlation Matrix")
plt.show()

#################### COMMUTE TIME IN ZIPS WITH VS WITHOUT METRO STATIONS ####################

# COMPARE THE AVG COMMUTE TIME FOR: zips that have at least one station and zips in the city that do not have a station
# DO ZIPS SERVED BY METRO STATIONS HAVE SHORTER COMMUTES ON AVERAGE?

# Use your ZIP-level dataset (zip_full merged with commute & income)
zip_stats = final_data.copy()
zip_stats["has_station"] = zip_stats["station_count"] > 0
zip_stats.groupby("has_station")["mean_commute_time"].mean()

binary_corr = zip_stats[["mean_commute_time", "has_station"]].corr()
sns.heatmap(binary_corr, annot=True, cmap="Reds", square=True)
plt.title("Correlation Matrix")
plt.show()

#################### SCATTERPLOT: INCOME VS COMMUTE TIME ####################

# DO WEALTHIER ZIP CODES HAVE SHORTER OR LONGER COMMUTES

plt.figure(figsize=(8,6))
plt.scatter(zip_stats["median_income"], zip_stats["mean_commute_time"])
plt.xlabel("Median Household Income")
plt.ylabel("Mean Commute Time (minutes)")
plt.title("Commute Time vs Income by ZIP Code")
plt.show()

### REGRESSION ### 

## COMMUTE TIME ~ INCOME + STATION COUNT 
## AFTER ACCOUNTING FOR INCOME, DOES STATION DENSITY MATTER?

# MAKING SURE DATA IS CLEAN AND AGGREGATED AT ZIP LEVEL 

# Loading the ZIP-level dataset created in your prep file
final_data = pd.read_csv("data/final_data_cleaned.csv")

# Dropping any missing values needed for regression
zip_clean = final_data.dropna(subset=["mean_commute_time", "median_income", "station_count"])

# Defining X and y
X = zip_clean[["median_income", "station_count"]]
X = sm.add_constant(X)     # adds intercept
y = zip_clean["mean_commute_time"]

# Fit the regression
model = sm.OLS(y, X).fit()

print(model.summary())


