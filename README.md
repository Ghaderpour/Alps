# Elevation-Dependent Coupling Between Land Surface Temperature and Snow Cover in the Alpine Conifer and Mixed Forests Ecoregion: A Multi-Scale Trend and Cross-Wavelet Analysis

This repository contains the code and data used in the manuscript:

**"Elevation-Dependent Coupling Between Land Surface Temperature and Snow Cover in the Alpine Conifer and Mixed Forests Ecoregion: A Multi-Scale Trend and Cross-Wavelet Analysis"**

## Repository Contents

### 1. Pre-processed-Datasets.zip

This folder contains the pre-processed datasets used in this study. In other words, this folder contains the monthly ecoregion-averaged datasets (2000–2025).

The following excel files contain ecoregion-averaged monthly observations for each calendar month from 2000 to 2025:
  * MODIS_SnowCover_Alps.xlsx
  * MODIS_DaytimeLST_Alps.xlsx
  * MODIS_NighttimeLST_Alps.xlsx

Each file is organized by calendar month (January–December) which contains 26 annual observations (2000–2025) representing the spatial average over the entire Alpine Conifer and Mixed Forests ecoregion. These datasets were used to generate the ecoregion-wise analyses reported in Tables 2, 4, and 5.

The following excel file contains the annual pixel count of each MODIS land cover class (LC_Type1) within the Alpine Conifer and Mixed Forests ecoregion for 2001–2024. These statistics were used to quantify long-term land cover changes.
  * MODIS_LC_Statistics_Alps.xlsx

The following excel files contain 312 consecutive monthly observations spanning January 2000 to December 2025, where each value is the spatial average over the entire Alpine Conifer and Mixed Forests ecoregion:
  * MODIS_SnowCover_Alps_Jan2000_Dec2025.xlsx
  * MODIS_LST_Alps_Jan2000_Dec2025.xlsx

These continuous time series were used as inputs for the least-squares cross-wavelet analysis (LSCWA) to produce the cross-spectrograms presented in Figure 7.

### 2. Table_Results

This folder contains the Excel files used to generate the tables presented in the manuscript and Supplementary Materials.

Ecoregion-averaged monthly median values, Theil–Sen slopes, and trend classifications for MODIS snow cover, daytime LST, and nighttime LST (2000–2025). Used to generate Table 2:
* Table2_Monthly_Theil_Sen_MeanSpatial_Alps.xlsx

Monthly Pearson correlation coefficients between elevation and the median snow cover, daytime LST, and nighttime LST maps. Used to generate Table 3:
* Table3_PearsonCorrelation_LSTElevation_SnowCoverElevation.xlsx

Monthly Pearson correlation coefficients between ecoregion-averaged snow cover and daytime/nighttime LST time series (2000–2025). Used to generate Table 4:
* Table4_Monthly_MODIS_Snow_LST_Correlation_Alps.xlsx

Annual pixel counts and Theil–Sen trend statistics for all MODIS land cover classes (2001–2024). Used to generate Table 5.
* Table5_MODIS_LC_Theil_Sen_Statistics_Alps.xlsx

Elevation-dependent spatial coupling analysis between significant land cover changes and significant snow cover trends. The workbook contains the results presented in Table 6 (main manuscript) and Table S1 (Supplementary Materials).
* Tables6andS1_MODIS_LC_SnowCover_ElevationAnalysis.xlsx

Elevation-dependent spatial coupling analysis between significant land cover changes and significant nighttime LST trends. The workbook contains the results presented in Table 7 (main manuscript) and Table S2 (Supplementary Materials).
* Tables7andS2_MODIS_LC_NighttimeLST_ElevationAnalysis.xlsx

Distribution of annual phase-delay classes between snow cover and daytime/nighttime LST within four elevation bands for pixels exhibiting annual coherency greater than 10%. Phase differences are grouped into approximately one-month intervals and used to generate Table S3 in the Supplementary Materials:
* TableS3_ElevationBased_PhaseClassification.xlsx



### 3. Raster.zip

This archive contains GeoTIFF raster datasets generated in the study, including:

* Monthly median maps
* Trend (Sen's slope) maps
* Snow cover–LST correlation maps
* Coherency maps
* Additional spatial analysis products

### 4. Python Scripts
#### 1. Monthly_Median_TheilSen_Maps.py

Generates monthly median and pixel-wise Theil–Sen slope maps for MODIS snow cover and land surface temperature (LST) (2000–2025). Produces the raster outputs used in Figures 3, 4, and Figures S1–S6.

#### 2. Monthly_Ecoregion_TheilSen.py

Computes the monthly median, Theil–Sen slope, and trend classification for ecoregion-averaged snow cover, daytime LST, and nighttime LST time series. Produces Table 2.

#### 3. Pearson_Elevation_LST.py

Calculates the pixel-wise Pearson correlation between elevation and monthly median snow cover or LST rasters for each calendar month. Produces Table 3.

#### 4. MODIS_LandCover_TheilSen.py

Computes the median area, Theil–Sen slope, and trend classification for each MODIS land cover class (2001–2024) using ecoregion-wide annual statistics. Produces Table 5.

#### 5. LC_LST_ElevationAnalysis.py

Performs the elevation-dependent spatial overlap analysis between significant land cover trends and significant nighttime LST warming or snow cover decline. Produces Tables 6, 7, S1, S2, and supports the analyses presented in Figure 10.

## Study Period

2000–2025

## Data Sources

* MODIS Snow Cover Products
* MODIS Land Surface Temperature (Daytime and Nighttime) Products
* MODIS Land Cover (LC_Type1)
* SRTM Digital Elevation Model (DEM)

