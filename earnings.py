#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 14:32:18 2023

@author: yuliabychkovska
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import requests
import seaborn as sns


api = 'https://api.census.gov/data/2018/acs/acs5'
for_clause = 'county:*' #indicating the kind of units to return and selecting subsets of possible records
in_clause = 'state:36' #'in' is used to limit the selected geographic units to the larger geographic entity
key_value = 'd4d1df4e9b73f11c6b9c2cf29192f852527e9db0' #Census API

payload  = {'get': 'NAME,B20002_001E', 'for':for_clause, 'in':in_clause, 'key':key_value}
response = requests.get(api, payload) 
#building an HTTPS query string, sending it to the API endpoint, and collecting the respose

row_list = response.json() #returning list of rows
colnames = row_list[0] #setting variable to the first row
datarows = row_list[1:] #setting variable to the remaining rows

earnings = pd.DataFrame(columns=colnames,data=datarows) #converting data into a Pandas dataframe
earnings = earnings.set_index('NAME') #creating a dataframe for all counties in New York
 
earnings['GEOID'] = earnings['state']+ earnings['county'] #concatenating the columns of earnings

earnings['median'] = earnings['B20002_001E'].astype(float)/1000 #creating a numeric column, results in thousands of $

earnings.to_csv('earnings.csv', index=False) #creating a csv file without saving

#%% drawing a histogram
fig, ax1 = plt.subplots(dpi=300)
sns.histplot(data=earnings, x="median", stat="density", ax=ax1) #drawing an histogram of median earnings
#stat indicates that the Y axis should be the probability density
sns.kdeplot(data=earnings, x="median", shade=True, ax=ax1) #adding a kernel density estimate to the figure
#shade option causes the area below the curve to be shaded
ax1.set_xlabel('Median Income in Thousands')
fig.tight_layout()
fig.savefig('earnings_hist.png')

#%% creating a trimmed-down dataframe
trimmed = ['GEOID','median']
trim = earnings[trimmed]

#%% geopandas
geodata = gpd.read_file('cb_2019_us_county_500k.zip')
geodata = geodata.query("STATEFP=='36'") #filtering `geodata` down to New York counties
geodata = geodata.merge(trim,on='GEOID',how='left',validate='1:1',indicator=True) #merging the data 
print(geodata['_merge'].value_counts()) #checking if all counties matched
geodata.drop(columns='_merge',inplace=True) #dropping a column

geodata.to_file("counties.gpkg",layer="earnings") 
#write out `geodata` to a geopackage file called `"counties.gpkg"`. Set the layer to `"earnings"










