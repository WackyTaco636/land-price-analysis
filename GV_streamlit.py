import streamlit as st
import altair as alt
import pandas as pd
from pathlib import Path
from streamlit_folium import folium_static
######################
from GV_Folium_2Scale_DE import propmap
from GV_IN_DE_DataCleanse import df, dfk, dfc, vlucnts, zip_samples
from GV_linear_regression_realtime import zipcode_analysis
######################

st.title('Land Price Analysis of German Zip-Codes')

st.write('Map generated from',len(df),'offers (Green: up to 120 EUR/m²; Red: above 120 EUR/m²)')

folium_static(propmap)

st.markdown('The generated map above shows the general distribution of square-meter prices of land in zip-codes in which data could be gathered. Zip-codes colored green represent prices up to 120 EUR per square-meter and zip-codes colored red represent prices above this range.')

st.markdown('The data used for this project was scraped from offers posted online. The original dataset can be viewed in the table below.')

st.write('Database currently housing',len(df),'rows of scraped offers:',df)

st.markdown('___')

st.subheader('Overview of land prices by zip-code')

st.write('This next section will take a closer look at the individual zip-codes to give you an overview of the area/price distribution followed by a fair-price valuation. Which Postcode do you want to examine (tip: use the interactive map of Germany above and mouse-over zip-codes you are interested in)? \n\n Use the slider to select zip-codes with a sufficient amount of samples if you want to narrow your options while increasing the accuracy of the analysis and overview.\n\nNote: the current minimum sample size for the fair-price valuation of land for the selected zip-code is set to 3, and is not reflected in the map of Germany above (all samples in the database).')

samp_size = st.slider('Minimum Sample Size',min_value=3,max_value=int(vlucnts.max()))

zipcodes = zip_samples(samp_size)

st.write('Currently, there are',len(zipcodes),'zip-codes available for closer analysis based on your selection of minimum sample size.')

option = st.selectbox('Select the zip-code you would like to investigate:',zipcodes)

st.subheader('Distribution of property size and price of land in zip-code')

d = zipcode_analysis(option)

st.write(len(d),'properties available for analysis in the selected zip-code')

c = alt.Chart(d).mark_circle().encode(x='area', y='price')

st.altair_chart(c, use_container_width=True)

st.subheader('Fair-price valuation of offers in zip-code')

#### NOTE: need to add code that makes negative gradients statistically insignificant

st.write('The dataset has an r² score of:',str(round(d['r2_score'][0],2)),', and a gradient of:',str(round(d['coefficient'][0][0])),'.')

if d['r2_score'][0] < 0.5 :
    st.write('**WARNING: an r2_score lower than 0.5 indicates a statistically insignificant fair-price valuation**')

if d['coefficient'][0] < 0 :
    st.write('**WARNING: a negative gradient indicates a statistically insignificant fair-price valuation**')

st.write(d.loc[:,['offer','rowzip','area','price','fairprice']].round())

#### Story Questions ####

# min / max / avg / std  ->  Maybe dynamically on a map with federal states?
# i.e. which states have the most expensive properties, variances between property prices and so forth
# ->> Population as a driver?

# Where are the prices least rational (low r2_score)?
