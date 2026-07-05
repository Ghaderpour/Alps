"""
This script computes the monthly median, Theil–Sen slope, and trend classification (increasing, decreasing, or no trend) 
for ecoregion-averaged MODIS snow cover, daytime LST, and nighttime LST time series. 
For each calendar month, the Theil–Sen slope is estimated using a 95% confidence interval, 
and trends are classified according to whether the confidence interval excludes zero.

Outputs:

Table 2 in the manuscript, reporting the monthly median values, Theil–Sen slopes, 
and trend classifications for the Alpine Conifer and Mixed Forests ecoregion.

Note:
The script accepts any monthly ecoregion-averaged time series organized by calendar month and can 
therefore be readily adapted to other variables with the same format.

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
import os

# ==============================================================
def compute_sen_trends(excel_files, out_excel):

    months = ['Jan','Feb','Mar','Apr','May','Jun',
              'Jul','Aug','Sep','Oct','Nov','Dec']

    writer = pd.ExcelWriter(out_excel, engine='xlsxwriter')

    for file in excel_files:

        df = pd.read_excel(file, index_col=0)

        results = []

        for m in months:

            ts = df[m].values.astype(float)

            # Remove NaNs
            valid = np.isfinite(ts)

            if np.sum(valid) < 5:
                slope = np.nan
                median = np.nan
                trend = "no data"

            else:
                y = ts[valid]
                x = np.arange(len(ts))[valid]

                # -------------------------
                # Median
                # -------------------------
                median = np.nanmedian(y)

                # -------------------------
                # Theil-Sen slope + CI
                # -------------------------
                slope, intercept, lower, upper = theilslopes(y, x, 0.95)

                # -------------------------
                # Trend classification
                # -------------------------
                if lower > 0:
                    trend = "increasing"
                elif upper < 0:
                    trend = "decreasing"
                else:
                    trend = "no trend"

            results.append([m, median, slope, trend])

        result_df = pd.DataFrame(
            results,
            columns=['Month', 'Median', 'Sen_Slope', 'Trend']
        )

        # Sheet name from file
        sheet_name = os.path.basename(file).replace('.xlsx','')
        result_df.to_excel(writer, sheet_name=sheet_name, index=False)

        print(f"Processed: {file}")

    writer.close()

    print("\nAll results saved to:", out_excel)


# ==============================================================
excel_files = [
    r"D:\Alps\Preprocessed_Datasets\MODIS_SnowCover_Alps.xlsx",
    r"D:\Alps\Preprocessed_Datasets\MODIS_DaytimeLST_Alps.xlsx",
    r"D:\Alps\Preprocessed_Datasets\MODIS_NighttimeLST_Alps.xlsx"
]

out_excel = r"D:\Alps\Table_Results\Table2_Monthly_Theil_Sen_MeanSpatial_Alps.xlsx"

compute_sen_trends(excel_files, out_excel)