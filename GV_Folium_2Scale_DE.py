#### This versions has no black postal codes ####
import requests
import folium
import pandas as pd
import json
#########################################
from GV_IN_DE_DataCleanse import dfk
#########################################

pivot = dfk.pivot_table(index =['zip'],
                       values =['sqmprice'],
                       aggfunc ='mean')
# print(pivot.index)

pivot1 = pivot[pivot['sqmprice'] <= 120 ]
# print(pivot1['sqmprice'].max())
pivot2 = pivot[pivot['sqmprice'] >= 120.01 ]
# print(pivot2['sqmprice'].min())

############## REMOVE UNECESSARY ZIP CODES ###############
plzmap = '/home/ec2-user/land-price-analysis/plz-5stellig.geojson'
# load GeoJSON
with open(plzmap, 'r') as jsonFile :
    data = json.load(jsonFile)
tmp = data

# /!\ CRAPPY REPETITIVE CODE /!\
#### PIVOT 1 ####
# remove zips that are not included in data
geozips = []

for i in range(len(tmp['features'])) :
    if tmp['features'][i]['properties']['plz'] in list(pivot1.index.unique()) :
        geozips.append(tmp['features'][i])

# print(geozips)

# creating new JSON object
new_json = dict.fromkeys(['type','features'])
new_json['type'] = 'FeatureCollection'
new_json['features'] = geozips

# save JSON object as updated-file
open('pivot1-5stellig_GV_DE.geojson', 'w').write(
    json.dumps(new_json, sort_keys=True, indent=4, separators=(',', ': '))
)

newplzmap1 = '/home/ec2-user/land-price-analysis/pivot1-5stellig_GV_DE.geojson'

#### PIVOT 2 ####
geozips = []

for i in range(len(tmp['features'])) :
    if tmp['features'][i]['properties']['plz'] in list(pivot2.index.unique()) :
        geozips.append(tmp['features'][i])

# print(geozips)

# creating new JSON object
new_json = dict.fromkeys(['type','features'])
new_json['type'] = 'FeatureCollection'
new_json['features'] = geozips

# save JSON object as updated-file
open('pivot2-5stellig_GV_DE.geojson', 'w').write(
    json.dumps(new_json, sort_keys=True, indent=4, separators=(',', ': '))
)

newplzmap2 = '/home/ec2-user/land-price-analysis/pivot2-5stellig_GV_DE.geojson'

#print(newplzmap2)
############## CREATE FOLIUM MAP ###############

propmap = folium.Map(location=[51.079375, 10.419608], tiles="Stamen Toner", zoom_start=6)

layer1 = folium.Choropleth(geo_data=newplzmap1,
             data=pivot1,
             columns=[pivot1.index, 'sqmprice'],
             key_on='feature.properties.plz',
             fill_color='Greens', fill_opacity=0.7, line_opacity=0.2,
             bins = [0,5,10,20,40,60,80,100,121],
             legend_name='Square Meter Price (EUR)',
             highlight = True).add_to(propmap)

# add labels indicating data on postcode
style_function = "font-size: 15px; font-weight: bold"
layer1.geojson.add_child(
    folium.features.GeoJsonTooltip(['plz'], style=style_function, labels=True))

layer2 = folium.Choropleth(geo_data=newplzmap2,
             data=pivot2,
             columns=[pivot2.index, 'sqmprice'],
             key_on='feature.properties.plz',
             fill_color='Reds', fill_opacity=0.7, line_opacity=0.2,
             bins = [120,250,500,750,1000,1250,2500,5000,15000],
             legend_name='Square Meter Price (EUR)',
             highlight = True).add_to(propmap)

# add labels indicating data on postcode
layer2.geojson.add_child(
    folium.features.GeoJsonTooltip(['plz'], style=style_function, labels=True))

propmap.save('/home/ec2-user/land-price-analysis/GV_DE.html')
