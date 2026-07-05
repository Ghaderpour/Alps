# Elevation-Dependent Coupling Between Land Surface Temperature and Snow Cover in the Alpine Conifer and Mixed Forests Ecoregion: A Multi-Scale Trend and Cross-Wavelet Analysis

This repository contains the code and data used in the manuscript:

**"Elevation-Dependent Coupling Between Land Surface Temperature and Snow Cover in the Alpine Conifer and Mixed Forests Ecoregion: A Multi-Scale Trend and Cross-Wavelet Analysis"**

## Repository Contents

### Pre-processed-Datasets.zip

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

### 1. TimeSeries.zip

This archive contains annual time series (2000–2025) for each calendar month derived from MODIS products, including:

* MODIS Snow Cover
* MODIS Daytime Land Surface Temperature (LST)
* MODIS Nighttime Land Surface Temperature (LST)
* MODIS Land Cover (LC_Type1)

It also includes the outputs of trend and statistical analyses used in the study.

### 2. Raster.zip

This archive contains GeoTIFF raster datasets generated in the study, including:

* Monthly median maps
* Trend (Sen's slope) maps
* Snow cover–LST correlation maps
* Coherency maps
* Additional spatial analysis products

### 3. Python_Code.zip

Python scripts used for data preprocessing, statistical analyses, trend estimation, correlation analysis, coherency analysis, and figure generation.

## Study Period

2000–2025

## Data Sources

* MODIS Snow Cover Products
* MODIS Land Surface Temperature (Daytime and Nighttime) Products
* MODIS Land Cover (LC_Type1)
* SRTM Digital Elevation Model (DEM)

