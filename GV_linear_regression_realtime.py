import sqlite3
import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.metrics import r2_score
#####################################
from GV_IN_DE_DataCleanse import df, dfk, dfc, vlucnts
#from GV_streamlit import zipcodes as zips
#####################################

### Prepare the x and y parameters to train the model below (remember, we want to train the model not on all available postcodes but on the samples contained within a postcode)
def zip_data(z) :
    data = dfc[dfc['zip'] == z]
    # print('rowzip:',rowzip,'len:',len(data),data)
    x_parameter = []
    y_parameter = []
    for offer_area,offer_price in zip(data['area'],data['price']) :
        x_parameter.append([float(offer_area)])
        y_parameter.append(float(offer_price))

    return x_parameter,y_parameter

### Function for Fitting data to Linear model - predict_value is the area of one sample in the zip-code population
def linear_model_main(x_parameter,y_parameter,predict_value) :
    regr = linear_model.LinearRegression() # call sklearn.linear_model and select LinearRegression Method
    regr.fit(x_parameter,y_parameter) # fit the data to the model
    predict_outcome = regr.predict(predict_value) # use the predict function to predict value
    predictions = {}
    predictions['intercept'] = regr.intercept_
    predictions['coefficient'] = regr.coef_
    predictions['predicted_value'] = predict_outcome
    predictions['r2_score'] = r2_score(y_parameter, regr.predict(x_parameter))
    return predictions

#### NOTE: need to add code that makes negative gradients statistically insignificant

### The 'Query' in the code: 'Using zip_data() and linear_model_train, return the estimated fair price of property for every single offer'
def zipcode_analysis(z) :
    dict = {'offer':[],'rowzip':[],'area':[],'price':[],'fairprice':[],'r2_score':[],'coefficient':[]}
    for offer, rowzip, area, price in zip(dfc['offer'],dfc['zip'],dfc['area'],dfc['price']) :
        if rowzip == z :

            x,y = zip_data(rowzip)
            predict_value = [[area]]
            result = linear_model_main(x,y,predict_value)

            dict['offer'].append(offer)
            dict['rowzip'].append(rowzip)
            dict['area'].append(area)
            dict['price'].append(price)
            dict['fairprice'].append(result['predicted_value'])
            dict['r2_score'].append(result['r2_score'])
            dict['coefficient'].append(result['coefficient'])

    dffp = pd.DataFrame(dict)
    dffp['fairprice'] = dffp['fairprice'].str[0]

    return dffp
    # print(dffp['fairprice'])
# dffp.to_csv('/home/chris/Documents/01_Projects/01_Grundstückvaluierung/04_Analysis/01_Data/dffp.csv')
