# finalproject

Welcome!

----------------------------------------------LAUNCHING WEBAPP-------------------------------------------------<br />
Access to our webapp uploaded on the free server (pythonanywhere)! 
http://hajime.pythonanywhere.com/myapp/ <br />
(Or of course you can run the django files. Just enter "python manage.py runserver" in your terminal and access http://127.0.0.1:8000/myapp/)


The purpose of this webapp is to provide useful information about certain community area to those who are wondering which community area to live in Chicago.<br />

After enjoying the top page, proceed to "Community Area Fact Checker". When you choose a community area, you will find the following four outputs:<br />
  + The table of criminal indiator (crimes per 1,000 population in 2015) <br />
    The data of the community area, Chicago overall, and the rank of the community area in each crime type.<br />
  + Homicide map in 2015<br />
    To ensure fast and comfortable access speed, we only provide the data pertaining to Homicides, but you will be able to grasp the idea about which community area is dangerous by using this most typical and serious crime type. You will have to look for a community area manually.
  + The bar graph of educational indicator 2008-2012 (% aged 25+ without high school diploma)<br />
    You will be able to compare the educational situation across community areas by using "% aged 25+ without high school diploma". The bars of the community area you choose and Chicago will be highlighted.
  + The bar graph of poverty indicator 2008-2012 (% households below poverty)<br />
    You will be able to compare the poverty indicator across community areas by using "% households below poverty". The bars of the community area you choose and Chicago will be highlighted.<br />

If you only know "neighborhood" instead of "community area", click "Look for" right below the pulldown menu and look for it.<br />

If you want to know about other community areas, click "Search again" link located right above the crime table.<br />
<br />
<br />

---------------------------------------------------SOURCES-----------------------------------------------------<br />
We used two sources from the City of Chicago and one from certain research center:<br />
  + "Crime Data 2001-"<br />
     City of Chicago Data Portal<br /> (https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-present/ijzp-q8t2/data)<br />

  + "Chicago Community Areas by Population" <br />
     Social Impact Research Center-A Heartland Alliance Program (http://www.ilpovertyreport.org/sites/default/files/uploads/Chicago%20Community%20Area%20Indicators,%202000-2012_140321.pdf)<br />

  +  "Census Data - Selected socioeconomic indicators in Chicago, 2008 – 2012" <br />
     City of Chicago Data Portal (https://data.cityofchicago.org/Health-Human-Services/Census-Data-Selected-socioeconomic-indicators-in-C/kn9c-c2s2)<br />
<br />
<br />

--------------------------------------Clearing/Reducing Process of Data-----------------------------------------<br />
You can find the script in finalproject-Ernesto-Juan-Hajime/static/dataclean.py.<br />
<br />
Chicago Crime Data was the most difficult one to process since it was the very
primitive raw data which has each individual case. I did the following:<br />
  + Read the csv file into pd.dataframe<br />
  + Extracted the columns I need for this Project<br />
  + Extracted the data of 2015<br />
  + Dropped rows with missing values <br />
  + For each community area, grouped by crime types and counted the incidents<br />
  + Converted the data from "number of crimes" into "number of crimes per 1,000 residents" by using the data of community area population, so as to allow for comparison with other community areas<br />
  + Concat all the dataframe based on each community area<br />
  + (You can find the scripts ("dataclean.py") at "finalproject-Ernesto-Juan-Hajime/static")

For the homicide map purpose: <br />
  + Cleaned the data with the scripts("01dataclean_for_map.py"), and produced "02map.csv"<br />
  + Process "02map.csv", create a html file with the scripts("03createmap.py")<br />
  + (You can find the scripts at "finalproject-Ernesto-Juan-Hajime/static/for_map") <br />

On the other hand, the census data were already nicely processed. The information is grouped by community areas and has % of various indicators. What I did is:<br />
  + Read the csv file into pd.dataframe<br />
  + Extracted the columns I need for this project <br />
  + Filled the empty cell ("NA") with "0"<br />
  + Cleaned datatype (e.g. "community area number" was somehow converted to floats.)<br />
<br />

And finally, I "concat"ed these two dataframes, rounded up to 2nd decimal place, and exported the dataframe to a csv file. I succeeded in reducing the total file size from about 1.5GB to 15KB.
<br />
<br />
<br />
<br />
<br />
<br />

---------------------------------------------(FOR TEAM MEMBERS)-------------------------------------------------<br />
First thing to do:
git clone git@github.com:hajimetada/finalproject-Ernesto-Juan-Hajime.git

Project Guideline:
https://harris-ippp.github.io/

Here is what we proposed to Jamie:
  "Our basic concept is to build a website which provides users valuable data (crime rate, average education, etc.) when they need to decide which area/neighborhood to live. Its functionality would be:<br />
    1. a user choose area/neighborhood<br />
    2. returns values (such as crime rate) of that neighborhood and Chicago overall<br />
    3. draws a graph which describe the trend of 2<br />
    4. (Hopefully) plots dots on neighborhood map<br />

  Our source is from Chicago crime data (2001-)(the one we used in the first assignment) and census data.
