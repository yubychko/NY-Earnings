"""
demo.py
Spring 2022 PJW

Demonstrate using geopandas for joining data onto a shapefile. To use
this script, download the Census shapefile cb_2019_us_state_500k.zip 
and the CSV file population.csv from the course Google Drive.
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

#%%
#
#  Read the shapefile and set the index to the state PO code
#

states = gpd.read_file("cb_2019_us_state_500k.zip")

states = states.set_index('STUSPS',drop=False)

print( '\nOriginal length:', len(states) )

#
#  Now filter out the states or equivalent entities that aren't part
#  of the contiguous (or conterminous) US. Note that the drop is being
#  done on the rows since the columns= argument wasn't used.
#

not_conus = ['AK','AS','GU','HI','MP','PR','VI']

conus = states.drop(not_conus)

print( '\nFiltered length:', len(conus) )

#%%
#
#  What's in conus?
#

print( 'number of rows, columns:', conus.shape )
print( 'columns:', list(conus.columns) )

#
#  Grab the row for a sample state, WV
#

wv = conus.loc['WV']
print( wv )

#
#  Get information about its geometry
#

wv_geo = wv['geometry']

print( 'Type of object:', type(wv_geo) )
print( 'Number of points:', len(wv_geo.exterior.coords) )

print( wv_geo )

#%%
#
#  Select the West Coast and draw a simple map
#

sel = conus.loc[['CA','OR','WA']]

fig, ax1 = plt.subplots(dpi=300)

sel.plot('NAME',cmap='Dark2',ax=ax1)

fig.tight_layout()
fig.savefig('west_coast.png')

#%%
#
#  Read the population data, being careful to keep the state
#  FIPS code as a string
#

pop = pd.read_csv('population.csv',dtype={'state':str})

#  Rename the state FIPS code to match the column name
#  in the county shapefile

pop = pop.rename(columns={'state':'STATEFP'})

#  Convert the population to millions and also compute the percentage

pop['mil'] = pop['B01001_001E']/1e6

pop['pct'] = 100*pop['mil']/pop['mil'].sum()
pop['pct'] = pop['pct'].round(2)

#  Select the variables to join onto the shapefile and trim down the
#  dataframe

sel_vars = ['STATEFP','mil','pct']

trim = pop[sel_vars]

#%%
#
#  Now merge the population data onto the shapefile.
#

conus = conus.merge(trim,on='STATEFP',how='left',validate='1:1',indicator=True)

print( conus['_merge'].value_counts() )
conus.drop(columns='_merge',inplace=True)

#
#  The index is discarded during the merge, so reset it
#

conus = conus.set_index('STUSPS')

#%%
#
#  Write it out as a geopackage file. Put the data into a layer
#  called states. Dis
#

conus.to_file("conus.gpkg",layer="states")

#%%
#
#  Now build a layer of WV and all states it touches
#

touches_wv = conus.touches(wv_geo)
touches_wv.loc['WV'] = True

near_wv = conus[ touches_wv ]

near_wv.plot('NAME',cmap='Dark2')

near_wv.to_file("conus.gpkg",layer="near_wv")

