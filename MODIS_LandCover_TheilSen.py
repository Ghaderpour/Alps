"""
This script computes the median area, Theil–Sen slope, and trend classification (increasing, decreasing, or no trend) 
for each MODIS land cover class using annual ecoregion-wide land cover statistics (2001–2024). 
The Theil–Sen slope is estimated with a 95% confidence interval, and trends are classified according 
to whether the confidence interval excludes zero.

Outputs:

Table 5 in the manuscript, summarizing long-term trends for all MODIS land cover classes across 
the Alpine Conifer and Mixed Forests ecoregion.

Note:
The script is designed for annual land cover statistics but can be readily adapted to other ecoregion-wide 
annual time series organized by class or category.


Citation:
This script is provided for research and educational purposes and is free to use and modify. 
If you use this script or adapt it in your work, please acknowledge the authors by citing:
Ghaderpour, E., et al. (2026). Elevation-Dependent Coupling Between Land Surface Temperature and Snow Cover 
in the Alpine Conifer and Mixed Forests Ecoregion: A Multi-Scale Trend and Cross-Wavelet Analysis. 
Ecological Informatics (2026)

"""

import pandas as pd
import numpy as np
from scipy.stats import theilslopes

# ============================================================
# INPUT / OUTPUT
# ============================================================

input_excel = r"D:\Alps\Preprocessed_Datasets\MODIS_LC_Statistics_Alps.xlsx"

output_excel = r"D:\Alps\Table_Results\Table5_MODIS_LC_Theil_Sen_Statistics_Alps.xlsx"

# ============================================================
# READ AREA SHEET
# ============================================================

df = pd.read_excel(input_excel, sheet_name="Area_km2")

# ============================================================
# YEARS
# ============================================================

years = df["Year"].values

# ============================================================
# LAND COVER CLASSES
# ============================================================

classes = [col for col in df.columns if col != "Year"]

# ============================================================
# OUTPUT LIST
# ============================================================

results = []

# ============================================================
# PROCESS EACH LAND COVER CLASS
# ============================================================

for lc in classes:

    print(f"Processing: {lc}")

    # --------------------------------------------------------
    # Time series
    # --------------------------------------------------------

    ts = df[lc].values.astype(float)

    # --------------------------------------------------------
    # Median Area
    # --------------------------------------------------------

    median_area = np.median(ts)

    # --------------------------------------------------------
    # Mann-Kendall + Sen's slope
    # --------------------------------------------------------

    
    slope, intercept, lower, upper = theilslopes(ts, years, 0.95)
    
    sens_slope = slope
    
    if lower > 0:
        trend = "increasing"
    elif upper < 0:
        trend = "decreasing"
    else:
        trend = "no trend"

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    results.append({
        "Land_Cover": lc,
        "Median_Area_km2": median_area,
        "Sens_Slope_km2_per_year": sens_slope,
        "Trend": trend
    })

# ============================================================
# CREATE OUTPUT DATAFRAME
# ============================================================

results_df = pd.DataFrame(results)

# ============================================================
# ROUND VALUES
# ============================================================

results_df["Median_Area_km2"] = results_df["Median_Area_km2"].round(2)

results_df["Sens_Slope_km2_per_year"] = \
    results_df["Sens_Slope_km2_per_year"].round(4)


# ============================================================
# SAVE TO EXCEL
# ============================================================

with pd.ExcelWriter(output_excel, engine="openpyxl") as writer:

    results_df.to_excel(
        writer,
        sheet_name="Trend_Statistics",
        index=False
    )

print("\nDone!")
print(f"Saved to:\n{output_excel}")