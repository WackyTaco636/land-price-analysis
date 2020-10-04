import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

### API connection to the database containing all of the scraped offers
conn = sqlite3.connect('''/home/ec2-user/land-price-analysis/GV_IN_DB_DE.sqlite''', timeout=3)
cur = conn.cursor()
### Select all offer data located in the main table 'Ads' and create a Pandas DataFrom without NaNs
tbl = cur.execute('''SELECT * FROM Ads''')
cols = [column[0] for column in tbl.description]
df = pd.DataFrame(tbl,columns=cols).round()
dfk = df[(df['marketingtype'] == 'Kauf') & (df['price'] > 0)]

dfc = dfk.loc[:,['offer','fed','zip','area','price','sqmprice']].dropna()

### Create a list of available zip-codes based on the scraped data where there are at least two samples for linear regression
vlucnts = dfc.zip.value_counts()

### Histogram of sqm land prices ### 
sqmprice_vlucnts = dfc.sqmprice.value_counts().sort_index()
# sqmprice_vlucnts = sqmprice_vlucnts.index.sort_values(ascending=False)
sqmprice_vlucnts = sqmprice_vlucnts[(sqmprice_vlucnts > 0 ) & (sqmprice_vlucnts.index < 250)]
print(sqmprice_vlucnts)

hist_sqm_vals = []
for key,val in sqmprice_vlucnts.items() :
    # print(key,val)
    for i in range(val) :
        hist_sqm_vals.append(key)
# print(x)

plt.hist(hist_sqm_vals, bins = 10)
hist_sqm =  plt.show()
#################################

feds = list(dfc.fed.sort_values(ascending=True).unique())
feds = ['Overall (Nationwide)'] + feds

# 'sample_size' is defined in GV_streamlit.py as the slider bar.
def zip_samples(sample_size) :
    zips = list(vlucnts[vlucnts >= sample_size].index.sort_values())
    return zips

# 'select_fed' is determined via dropdown in GV_streamlit.py.
def fed_summary(select_fed) :
    if select_fed != 'Overall (Nationwide)' :
        dfcf = dfc[(dfc['fed'] == select_fed)]
    else:
        dfcf = dfc
    dfcf = dfcf.loc[:,['area','price']]
    dfcf['sqmprice'] = dfcf['price'] / dfcf['area']
    desc = dfcf.describe().round().astype(int)
    return desc
