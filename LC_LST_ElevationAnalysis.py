"""
Description:
This script performs an elevation-dependent spatial overlap analysis between significant 
nighttime LST warming (Theil–Sen slope > 0) and significant MODIS land cover trends 
for each land cover class. 
Pixels are grouped into four elevation bands (0–1000 m, 1000–2000 m, 2000–3000 m, and >3000 m), 
and the script quantifies the spatial coincidence between nighttime LST warming and 
increasing or decreasing land cover within each elevation band. Results are exported to an Excel file.

Outputs:

Table 7 (main manuscript) for the most significant land cover classes.
Table S2 (Supplementary Materials) for all land cover classes.
Supports the elevation-dependent land cover–nighttime LST coupling analysis presented in Figure 10.

Note:By replacing the nighttime LST Theil–Sen rasters with the corresponding snow cover Theil–Sen rasters, 
this script can also be used to perform the elevation-dependent land cover–snow cover overlap analysis 
reported in Table 6 and Table S1.

Citation:
This script is provided for research and educational purposes and is free to use and modify. 
If you use this script or adapt it in your work, please acknowledge the authors by citing:

Ghaderpour, E., et al. (2026). Elevation-Dependent Coupling Between Land Surface Temperature and Snow Cover 
in the Alpine Conifer and Mixed Forests Ecoregion: A Multi-Scale Trend and Cross-Wavelet Analysis. 
Ecological Informatics (2026)
"""

import os
import numpy as np
import pandas as pd
from osgeo import gdal

# ==============================================================
# INPUTS
# ==============================================================

elevation_file = r"D:\Alps\Raster\DEM_downscaled\elevation_clip.tif"

lc_folder = r"D:\Alps\Raster\LC_TheilSen__PixelWise_Clipped"

lst_folder = r"D:\Alps\Raster\NighttimeLST_TheilSen_Clipped"

output_excel = r"D:\Alps\Table_Results\Tables7andS2_MODIS_LC_NighttimeLST_ElevationAnalysis.xlsx"

# ==============================================================
# READ TIFF
# ==============================================================

def read_raster(filename):

    ds = gdal.Open(filename)

    band = ds.GetRasterBand(1)

    arr = band.ReadAsArray().astype(float)

    nodata = band.GetNoDataValue()

    if nodata is not None:
        arr[arr == nodata] = np.nan

    ds = None

    return arr

# ==============================================================
# READ ELEVATION
# ==============================================================

elevation = read_raster(elevation_file)

# ==============================================================
# ELEVATION BANDS
# ==============================================================

bands = [

    (0,1000,"0-1000 m"),

    (1000,2000,"1000-2000 m"),

    (2000,3000,"2000-3000 m"),

    (3000,np.inf,">3000 m")

]

# ==============================================================
# FILE LISTS
# ==============================================================

lc_files = sorted([
    f for f in os.listdir(lc_folder)
    if f.lower().endswith(".tif")
])

lst_files = sorted([
    f for f in os.listdir(lst_folder)
    if f.lower().endswith(".tif")
])

results = []

print("-----------------------------------------")
print("Beginning Elevation Analysis")
print("-----------------------------------------")

#--------------------------------------------------------------------------------------------------------
# ==============================================================
# LOOP OVER NIGHTTIME LST MONTHS
# ==============================================================

for lst_file in lst_files:

    lst_name = os.path.splitext(lst_file)[0]

    print(f"\nProcessing {lst_name}")

    lst = read_raster(os.path.join(lst_folder, lst_file))

    # ----------------------------------------------------------
    # Significant warming pixels
    # ----------------------------------------------------------

    LSTsig = np.isfinite(lst)

    LSTinc = LSTsig & (lst > 0)

    # ----------------------------------------------------------
    # LOOP OVER LAND COVER CLASSES
    # ----------------------------------------------------------

    for lc_file in lc_files:

        lc_name = os.path.splitext(lc_file)[0]

        print("   ", lc_name)

        lc = read_raster(os.path.join(lc_folder, lc_file))

        LCsig = np.isfinite(lc)

        LCinc = LCsig & (lc > 0)

        LCdec = LCsig & (lc < 0)

        # ------------------------------------------------------
        # LOOP OVER ELEVATION BANDS
        # ------------------------------------------------------

        for emin, emax, label in bands:

            elev_mask = (
                np.isfinite(elevation)
                & (elevation >= emin)
                & (elevation < emax)
            )

            # ----------------------------------------------
            # Significant warming pixels in elevation band
            # ----------------------------------------------

            LSTband = LSTinc & elev_mask

            LSTbandPixels = np.sum(LSTband)

            # ----------------------------------------------
            # Overlaps
            # ----------------------------------------------

            LCInc = np.sum(
                elev_mask &
                LCsig &
                LCinc
            )

            LCDec = np.sum(
                elev_mask &
                LCsig &
                LCdec
            )

            # ----------------------------------------------

            IncInc = np.sum(
                LSTband &
                LCsig &
                LCinc
            )

            IncDec = np.sum(
                LSTband &
                LCsig &
                LCdec
            ) 

            # ----------------------------------------------
            # Save
            # ----------------------------------------------

            results.append({

                "LC_Class": lc_name,

                "LST_Month": lst_name,

                "Elevation_Band": label,

                "Nighttime LST Warming (Pixels)": LSTbandPixels,

                "LC Increase (Pixels)": LCInc,

                "LST Increase & LC Increase (Pixels)": IncInc,

                "LC Decrease (Pixels)": LCDec,

                "LST Increase & LC Decrease (Pixels)": IncDec

            })
#--------------------------------------------------------------------------------------------
# ==============================================================
# CREATE DATAFRAME
# ==============================================================

results_df = pd.DataFrame(results)

band_order = {
    "0-1000 m": 1,
    "1000-2000 m": 2,
    "2000-3000 m": 3,
    ">3000 m": 4
}

results_df["BandOrder"] = (
    results_df["Elevation_Band"]
    .map(band_order)
)

results_df = results_df.sort_values(
    by=[
        "LC_Class",
        "LST_Month",
        "BandOrder"
    ]
)

results_df.drop(columns="BandOrder", inplace=True)


# ==============================================================
# WRITE TO EXCEL
# ==============================================================

writer = pd.ExcelWriter(
    output_excel,
    engine="xlsxwriter"
)

results_df.to_excel(
    writer,
    sheet_name="ElevationAnalysis",
    index=False
)

workbook = writer.book
worksheet = writer.sheets["ElevationAnalysis"]

# ==============================================================
# FORMATS
# ==============================================================

header_format = workbook.add_format({

    'bold': True,

    'align': 'center',

    'valign': 'vcenter',

    'border': 1

})

cell_format = workbook.add_format({

    'align': 'center'

})

integer_format = workbook.add_format({

    'align': 'center',

    'num_format': '0'

})

percent_format = workbook.add_format({

    'align': 'center',

    'num_format': '0.00'

})

# ==============================================================
# WRITE HEADER
# ==============================================================

for col_num, value in enumerate(results_df.columns):

    worksheet.write(
        0,
        col_num,
        value,
        header_format
    )

# ==============================================================
# COLUMN WIDTHS
# ==============================================================

worksheet.set_column("A:A", 36, cell_format)

worksheet.set_column("B:B", 18, cell_format)

worksheet.set_column("C:C", 18, cell_format)

worksheet.set_column("D:G", 18, integer_format)

worksheet.set_column("F:F", 20, integer_format)

worksheet.set_column("H:H", 18, integer_format)

worksheet.set_column("I:I", 20, integer_format)


# ==============================================================
# FREEZE / FILTER
# ==============================================================

worksheet.freeze_panes(1, 0)

worksheet.autofilter(
    0,
    0,
    len(results_df),
    len(results_df.columns)-1
)

print("-----------------------------------------")
print("Elevation analysis finished.")
print("-----------------------------------------")

# ==============================================================
# CLOSE
# ==============================================================

writer.close()

print("\n==============================================")
print("Elevation-dependent analysis completed.")
print("==============================================")
print("Output:")
print(output_excel)
print("==============================================")