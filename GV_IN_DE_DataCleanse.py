import sqlite3
import pandas as pd

### API connection to the database containing all of the scraped offers
conn = sqlite3.connect('''/home/ec2-user/land-price-analysis/GV_IN_DB_DE.sqlite''', timeout=3)
cur = conn.cursor()
### Select all offer data located in the main table 'Ads' and create a Pandas DataFrom without NaNs
tbl = cur.execute('''SELECT * FROM Ads''')
cols = [column[0] for column in tbl.description]
df = pd.DataFrame(tbl,columns=cols).round()
dfk = df[df['marketingtype'] == 'Kauf']
# df = df[df['sqmprice'] > 10]
dfc = dfk.loc[:,['offer','zip','area','price']].dropna()
dfc = dfc[(dfc['area'] > 100) | (dfc['price'] > 1000)].round()
# dfc.to_csv('/home/chris/Documents/01_Projects/01_Grundstückvaluierung/04_Analysis/01_Data/dfc')
### Create a list of available zip-codes based on the scraped data where there are at least two samples for linear regression
vlucnts = dfc.zip.value_counts()

sample_size = 3

# 'sample_size' is defined in GV_streamlit.py as the slider bar.
def zip_samples(sample_size) :
    zips = list(vlucnts[vlucnts >= sample_size].index.sort_values())

    return zips
