"""
This script computes the Pearson correlation coefficient between elevation 
and the monthly median land surface temperature (LST) raster for each calendar month. 
The elevation raster and monthly LST rasters are first clipped to the Alpine Conifer and Mixed Forests ecoregion, 
after which valid pixels are extracted and Pearson's correlation coefficient, p-value, 
and number of valid pixels are calculated. The results are exported to an Excel file.

Note: This script is equally applicable to monthly median snow cover rasters by simply replacing the LST input folder.

Outputs: 
Table 3 (Elevation vs. daytime LST or nighttime LST or snow cover Pearson correlations, 
depending on the input raster folder) in the manuscript 

Citation:
This script is provided for research and educational purposes and is free to use and modify. 
If you use this script or adapt it in your work, please acknowledge the authors by citing:

Ghaderpour, E., et al. (2026). Elevation-Dependent Coupling Between Land Surface Temperature and Snow Cover 
in the Alpine Conifer and Mixed Forests Ecoregion: A Multi-Scale Trend and Cross-Wavelet Analysis. 
Ecological Informatics (2026)

"""

import os
import glob
import numpy as np
import pandas as pd
from osgeo import gdal
from scipy.stats import pearsonr

# ============================================================
# INPUTS
# ============================================================

# Folder containing 12 monthly LST rasters
lst_folder = r"D:\Alps\Raster\DaytimeLST_Median_2000_2025"

# Elevation raster already aligned to LST grid
elevation_file = r"D:\Alps\Raster\DEM_downscaled\DEM_downscaled_LST.tif"

# AOI shapefile
shapefile = r"D:\Alps\Raster\BorderAlps_Shapefile\Alps.shp"

# Output Excel file
output_excel = r"D:\Alps\Table_Results\Table3_PearsonCorrelation_DaytimeLST_Elevation.xlsx"

# Temporary clipped rasters
temp_folder = r"D:\Alps\RasterClip"

os.makedirs(temp_folder, exist_ok=True)

# ============================================================
# MONTH ORDER
# ============================================================

months = [
    "Jan", "Feb", "Mar", "Apr",
    "May", "Jun", "Jul", "Aug",
    "Sep", "Oct", "Nov", "Dec"
]

# ============================================================
# FUNCTION TO CLIP RASTER
# ============================================================

def clip_raster(input_raster, shapefile, output_raster):

    gdal.Warp(
        output_raster,
        input_raster,

        cutlineDSName=shapefile,
        cropToCutline=True,

        dstNodata=np.nan
    )

# ============================================================
# CLIP ELEVATION
# ============================================================

elev_clip = os.path.join(temp_folder, "elevation_clip.tif")

clip_raster(
    elevation_file,
    shapefile,
    elev_clip
)

# Read clipped elevation
elev_ds = gdal.Open(elev_clip)

elev_data = elev_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)

elev_nodata = elev_ds.GetRasterBand(1).GetNoDataValue()

# ============================================================
# FIND LST FILES
# ============================================================

lst_files = sorted(glob.glob(os.path.join(lst_folder, "*.tif")))

# ============================================================
# STORE RESULTS
# ============================================================

results = []

# ============================================================
# LOOP THROUGH MONTHLY LST FILES
# ============================================================

for month, lst_file in zip(months, lst_files):

    print(f"Processing: {month}")

    # --------------------------------------------------------
    # CLIP LST
    # --------------------------------------------------------

    lst_clip = os.path.join(
        temp_folder,
        f"{month}_clip.tif"
    )

    clip_raster(
        lst_file,
        shapefile,
        lst_clip
    )

    # --------------------------------------------------------
    # READ CLIPPED LST
    # --------------------------------------------------------

    lst_ds = gdal.Open(lst_clip)

    lst_data = lst_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)

    lst_nodata = lst_ds.GetRasterBand(1).GetNoDataValue()

    # --------------------------------------------------------
    # VALID MASK
    # --------------------------------------------------------

    valid_mask = np.isfinite(elev_data) & np.isfinite(lst_data)

    if elev_nodata is not None:
        valid_mask &= (elev_data != elev_nodata)

    if lst_nodata is not None:
        valid_mask &= (lst_data != lst_nodata)

    # --------------------------------------------------------
    # EXTRACT VALID PIXELS
    # --------------------------------------------------------

    elev_valid = elev_data[valid_mask]
    lst_valid = lst_data[valid_mask]

    # --------------------------------------------------------
    # PEARSON CORRELATION
    # --------------------------------------------------------

    r_value, p_value = pearsonr(
        elev_valid,
        lst_valid
    )

    # --------------------------------------------------------
    # SAVE RESULTS
    # --------------------------------------------------------

    results.append({
        "Month": month,
        "Pearson_r": r_value,
        "P_value": p_value,
        "N_pixels": len(elev_valid)
    })

# ============================================================
# SAVE TO EXCEL
# ============================================================

df = pd.DataFrame(results)

df.to_excel(output_excel, index=False)

print("\nDONE")
print("Saved:")
print(output_excel)