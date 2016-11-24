# finalproject

<Sources>
We used three sources as follows:<br />
"Crime Data 2001-"<br />
     City of Chicago Data Portal<br /> (https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-present/ijzp-q8t2/data)<br /
""

<Clearing/Reducing Process of Data>
You can find the script in finalproject-Ernesto-Juan-Hajime/static/dataclean.py.<br />
<br />
Chicago Crime Data was the most difficult one to process since it was the very
primitive raw data which has each individual case. What I did is:<br />
    • Read the csv file into pd.dataframe<br />
    • Extract columns I need for this Project<br />
    • Extract the data of 2015<br />
    • Drop rows with missing values <br />
    • For each community area, group by crime types and count the incidents<br />
    • Convert the data from "number of crimes" into "number of crimes per 1,000           residents" by using the data of communitya rea population, so as to allow for comparison with other community areas<br />
    • Concat all the dataframe based on each community area<br />
<br />
On the other hand, SelectedIndicators.csv was already nicely processed. It is grouped by community areas and has % of various indicators. What I did is:<br />
    • Read the csv file into pd.dataframe<br />
    • Extract columns I need for this project <br />
    • Fill the empty cell ("NA") with zero<br />
    • Clean up datatype (e.g. "community area number" was somehow converted to floats.)<br />
<br />
And finally, I concated these dataframes, rounded up to 2nd decimal place, and exported the dataframe to a csv file. I succeeded in reducing the total file size of about 1.5GB to 15KB.



--------------------------------(starting up)----------------------------------<br />
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
