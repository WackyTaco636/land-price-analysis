# land-price-analysis

*Imagine you are interested in a piece of land. Knowing how all the other plots of land are being offered in terms of price and size within a reasonable geographic area for comparison (e.g. within the same zip-code) will give you an indication whether that piece of land is overpriced or underpiced. If you go a step further and run linear regression analysis, you will be able to calculate the property's fair-price and use this to your advantage in price negotiations.*

**1) Introduction**

The land-price-analysis app is intended as both a showcase of my skills as a developer as well as a means to get a good overview and understanding of the German land-price-market as a whole all the way down to land-prices on a zip-code level. Python was used as the script language with SQL as the query language for the databases. 

Aside from providing graphical and statistical analysis to provide indications of where there is cheaper land to be bought, the main feature is the calculation of linear regression on properties on the zip code level, providing a fair-price valuation next to the offered amount posted online for that property.

In other words, instead of beginning negotiations based on the offerred price for the property, you will be able to enter negotiation for the price of that piece of land with a sound statistical approach.

***1.1) Assumptions***

The decision to analyse land properties was a personal one, as my wife and I are interested in purchasing land in the countryside somewhere in eastern Germany. The advantage that this dataset gives is simplicity for analysis. There are essentially 3 components of an offer being analysed: price, size (in square-metres) and geographic location (zip code).

The assumptions are simple and twofold: 

a) *Outside of large demand centres (cities), offered property will be comparibly cheaper. The gradient of the linear regression (price vs size within a zip-code) will be different depending on the zip-code, i.e., you may pay 500 EUR more per additional square-metre of land in a zip-code near Berlin, but may pay less per additional square-metre elsewhere.**

b) *The price of a property is directly correlated to it's size and thus comparison using linear regression will a statistically reliable fair-price valuation.*

**2) Methods of data gathering and statistical analysis**

The source of the data is the German real-estate platform immmonet.de. The source was selected as immonet.de provides the most online-listings for land in Germany.

The data was scraped using a script written in Python with BeautifulSoup4 and regex (amongst other modules) to target the html on the offer pages.

The statistics used for the analysis is both desciptive and inferrential. Concerning the fair-price analysis of offers linear regression was chosen as the the method providing the best fit after experimenting with K Nearest Neighbors Regresssion, and Neural Networks. 

The linear regression method is executed on a zip-code level in real-time (the user selects the postcode, the code runs the analyses on the data set). The results of the fair-price analysis of some zip-codes were unrealistic (e.g. fair-prices declining with increased size) due to very scattered samples located within a zip-code. To mitigate this two additional analyses were undertaken to inform the user of the validity of the data:

*a) Negative linear regression coefficients (gradients) are considered invalid and the user is informed via notification)*

*b) An r² analysis is conducted and if the result is below 50% the results are considered statistically insignificant and the user is informed of this via notification*

**2.1) Considerations for future analysis**

Currently, zip-codes with very scattered samples (i.e. the relation between price and size shows no correlation whatsoever between several properties in the same zip-code) are labelled as statistically insignificant and should therefore not be used to determine the fair-price.

These zip-codes could be examined closer in future using additional features, or perhaps other statistical methods in order to generate a statistically siginificant fair-price valuation for them.

**3) Explanation of app architecture**

The code-base is stored in the land-price-analysis repository on github and is executed on an AWS ec2 instance.
The git repository is cloned to the instance (/home/ec2-user/land-price-analysis).
Some working files are written and stored on AWS that are not visible on the git (these are files written by GV_Folium_2Scale_DE.py to generate the maps).

***3.1) App Code Base***

There are 6 files required to run this app (1 main app, 3 micro-services, 1 database, and 1 geoJSON map-file).

**GV_streamlit.py** -> The main app, which is the UI, that imports all micro-services required to visualize the data.

**GV_IN_DB_DE.sqlite** -> The database containing all of the scraped offers (for scraper, see: ...)

**GV_IN_DE_DataCleanse.py** -> Microservice that extracts and cleans the data from the sqlite3 database.

**GV_Folium_2Scale_DE.py** -> Microservice that generates a heat map of land prices per zipcode throughout Germany.

**GV_linear_regression_realtime.py** -> Microservice that runs a linear regression analysis on a selected zipcode.

**plz-5stellig.geojson** -> A map of Germany containing all zipcodes in geoJSON format.


**4) How to run it in AWS**

-> On your local machine, open a terminal and navigate to the folder containing the .pem file for access.

-> Connect to the ec2 instance via ssh (this is the current ssh login, but can change if e.g. another elastic IP is assigned to the instance): ssh -i "ChrisEC2.pem" ec2-user@ec2-35-179-72-37.eu-west-2.compute.amazonaws.com

-> Once connected to the ec2 via ssh, if the github repository land-price-analysis has not been cloned yet, run the command: sudo git clone https://github.com/WackyTaco636/land-price-analysis.git

-> If it has already been cloned, make sure you are using the most updated version by running following command: sudo git pull origin master.

-> To run the streamlit application cd to the land-price-analysis folder in the ssh and run: streamlit run GV_streamlit.py

**5) Troubleshooting**

***No write permissions in the folder (necessary for app to work)***

If the sreamlit app shows you a page with errorno13 concerning lack of write permissions, it's because the land-price-analysis folder appears not to contain writing permissions for ec2-user (note: the root user cannot and should not run python or streamlit commands). Check what the group permissions of the folder are with command: ls -l
The first column are the rights, the second the users, the third the user group land-price-analysis (to which ec2-user should belong). 
If you notice that the permissions look very different to the description above, use the following external documentation: https://stackoverflow.com/questions/27611608/ec2-user-permissions
