
# Mapping Median Earnings for New York Counties

## Summary

This project examines median earnings in New York counties over the last 12 months for the population 16 years and older who had any earnings.

## Input Data

The input file is **cb_2019_us_county_500k.zip** - a shapefile of US counties. The remaining data will be obtained from the Census via its API. 

## Deliverables

There are five deliverables: a script called **earnings.py** that requests data from the Census, saves a histogram of it in **earnings_hist.png**, joins it to a set of county polygons for New York counties, and writes out the result as a geopackage file called **counties.gpkg**; a QGIS project file called **earnings_map.qgz**; and a PNG file called **earnings_map.png** that will be a heat map of median earnings.
