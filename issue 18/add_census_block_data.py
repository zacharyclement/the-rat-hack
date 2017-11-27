#!/usr/bin/python
import pandas as pd
import geopandas
import geopandas.tools
from shapely.geometry import Point

# Note: you will need to install the rtree package - http://toblerity.org/rtree/install.html

print('imports finished')

data = pd.read_csv('output/inspections_geocoded.csv')
column_names = list(data.columns.values)

data['geometry'] = data.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)
data = geopandas.GeoDataFrame(data, geometry='geometry')
data.crs = {'init': 'epsg:4326'}

census_blocks = geopandas.GeoDataFrame.from_file('dc_2010_block_shapefiles/tl_2016_11_tabblock10.shp')
census_blocks.crs = {'init': 'epsg:4326'}

result = geopandas.tools.sjoin(data[['geometry']], census_blocks[['GEOID10', 'geometry']], how='left')

#############test###################
print 'result = '
print result
print ' ' 
print 'data = ' 
print data
print ' ' 
############################try converting to dataframes#####
df_result = pd.DataFrame(result)
df_data = pd.DataFrame(data)


print 'conversion'
###########error after this##################
###can't set result['geoid10'] to new column this way...

#data['census_block']=result['GEOID10']
##############################

concat = pd.concat([df_result, df_data], axis=1)
print 'merged is created'

#data = data[column_names + ['census_block']]

concat.to_csv('census_block.csv', index=False)