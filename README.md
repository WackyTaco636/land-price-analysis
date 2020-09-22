# land-price-analysis

1) Explanation of architecture

The code-base is stored in the land-price-analysis repository on github and is executed on an AWS ec2 instance.
The git repository is cloned to the instance (/home/ec2-user/land-price-analysis).
Some working files are written and stored on AWS that are not visible on the git (these are files written by GV_Folium_2Scale_DE.py to generate the maps).

2) How the app is built

There are 6 files required to run this app (1 main app, 3 micro-services, 1 database, and 1 geoJSON map-file).

GV_streamlit.py -> The main app, which is the UI, that imports all micro-services required to visualize the data.
GV_IN_DB_DE.sqlite -> the database containing all of the scraped offers (for scraper, see: ...)
GV_IN_DE_DataCleanse.py -> Microservice that extracts and cleans the data from the sqlite3 database.
GV_Folium_2Scale_DE.py -> Microservice that generates a heat map of land prices per zipcode throughout Germany.
GV_linear_regression_realtime.py -> Microservice that runs a linear regression analysis on a selected zipcode.
plz-5stellig.geojson -> A map of Germany containing all zipcodes in geoJSON format.

3) How to run it in AWS

