"""
This script computes the monthly median and Theil–Sen slope for each calendar month 
using the complete time series (2000–2025) of MODIS LST or snow cover. 
For each month (January–December), it generates a median raster representing the long-term 
monthly conditions and a pixel-wise Theil–Sen slope raster representing long-term trends.

Outputs:
The generated raster products are used to produce:
Figure 3 (snow cover Theil–Sen maps)
Figure 4 (nighttime LST Theil–Sen maps)
Figures S1 and S2 (snow cover median amd Theil-Sen maps)
Figures S3–S6 (LST median and daytime/nighttime Theil–Sen maps)

Note: The same script can be applied to either MODIS snow cover or MODIS nighttime LST by simply changing the input dataset.

Citation:
This script is provided for research and educational purposes and is free to use and modify. 
If you use this script or adapt it in your work, please acknowledge the authors by citing:
Ghaderpour, E., et al. (2026). Elevation-Dependent Coupling Between Land Surface Temperature and Snow Cover 
in the Alpine Conifer and Mixed Forests Ecoregion: A Multi-Scale Trend and Cross-Wavelet Analysis. 
Ecological Informatics (2026)
"""

import numpy as np
from osgeo import gdal, osr
import glob
import os
from scipy.stats import theilslopes
from datetime import datetime


# ==============================================================
def getSpatialRef(file):
    inRaster = gdal.Open(file)
    GeoT = inRaster.GetGeoTransform()
    Projection = osr.SpatialReference()
    Projection.ImportFromWkt(inRaster.GetProjection())
    return GeoT, Projection


# ==============================================================
def writeTiff(outFile, array, dataType, GeoT, Projection):
    rows, cols = array.shape

    driver = gdal.GetDriverByName("GTiff")
    ds = driver.Create(outFile, cols, rows, 1, dataType)
    ds.SetGeoTransform(GeoT)
    ds.SetProjection(Projection.ExportToWkt())

    band = ds.GetRasterBand(1)
    band.WriteArray(array)
    band.SetNoDataValue(np.nan)

    ds = None


# ==============================================================
def sen_slope_pixel(ts):
    ts = np.array(ts, dtype=float)

    valid = np.isfinite(ts)
    if np.sum(valid) < 3: # Thresholds 3 and 10 on these datasets produced the same results! 
        return np.nan

    y = ts[valid]
    x = np.arange(len(ts))[valid]

    try:
        slope, intercept, lower, upper = theilslopes(y, x, 0.95)

        # -------------------------------
        # significance test (95% CI)
        # -------------------------------
        if (lower > 0) or (upper < 0):
            return slope   # significant
        else:
            return np.nan  # NOT significant -> mask it

    except:
        return np.nan


# ==============================================================
def process_monthly_LST(ImageryDir, outDirSlope, outDirMedian):

    files = sorted(glob.glob(os.path.join(ImageryDir, "*.tif")))

    monthly_data = {m: [] for m in range(1, 13)}

    for file in files:

        ds = gdal.Open(file)

        # ---- Use only first band (daytime LST: 1 and nighttime LST: 2)
        img = ds.GetRasterBand(1).ReadAsArray().astype(float)

        # ---- Convert Kelvin to Celsius
        img = img - 273.15

        # ---- Remove invalid values
        img[img < -100] = np.nan
        img[img > 100] = np.nan

        basename = os.path.basename(file).replace(".tif", "")
        date_obj = datetime.strptime(basename, "%Y-%m-%d")
        month = date_obj.month

        monthly_data[month].append(img)

    GeoT, Projection = getSpatialRef(files[0])

    for month in range(1, 13):
        print(f'Processing month {month:02d}')

        stack = np.array(monthly_data[month])

        if stack.shape[0] == 0:
            continue

        rows, cols = stack.shape[1], stack.shape[2]

        # ------------------------------------------------------
        # Median image
        median_img = np.nanmedian(stack, axis=0)

        median_file = os.path.join(
            outDirMedian,
            f"LST_Day_Median_{month:02d}.tif"
        )

        writeTiff(
            median_file,
            median_img.astype(np.float32),
            gdal.GDT_Float32,
            GeoT,
            Projection
        )

        # ------------------------------------------------------
        # Sen slope image
        slope_img = np.full((rows, cols), np.nan, dtype=np.float32)

        for i in range(rows):
            for j in range(cols):
                ts = stack[:, i, j]
                slope_img[i, j] = sen_slope_pixel(ts)

        slope_file = os.path.join(
            outDirSlope,
            f"LST_Day_SenSlope_{month:02d}.tif"
        )

        writeTiff(
            slope_file,
            slope_img,
            gdal.GDT_Float32,
            GeoT,
            Projection
        )

        print(f"Month {month:02d} completed")

    return 1


# ==============================================================
if __name__ == "__main__":

    ImageryDir = r"D:\Alps\LST"
    outDirSlope = r"D:\Alps\Raster\DaytimeLST_TheilSen_2000_2025"
    outDirMedian = r"D:\Alps\Raster\DaytimeLST_Median_2000_2025"

    os.makedirs(outDirSlope, exist_ok=True)
    os.makedirs(outDirMedian, exist_ok=True)

    process_monthly_LST(ImageryDir, outDirSlope, outDirMedian)

    print("Complete!")
