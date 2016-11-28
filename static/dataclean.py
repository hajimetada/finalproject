# I'm going to integrate three files ("Crimes_-_2001_to_present.csv",
# "population_by_community_area.csv", and "SelectedIndicators.csv") into one
# file ("processed_data.csv").


import pandas as pd
# Read the csv file into df, using certain varibables.
df_crime = pd.read_csv("Crimes_-_2001_to_present.csv", usecols = ["Primary Type", "Community Area", "Year"])
# Extract the data of 2015 (2015 is the latest data which is complete),
# and drop rows with missing values.
df_crime = df_crime[df_crime["Year"]==2015].dropna()
# Drop rows if "Primary Type" is "NON-CRIMINAL" or "NON - CRIMINAL",
# since it's negligible information.
mask = df_crime["Primary Type"]=="NON-CRIMINAL"
mask &= df_crime["Primary Type"]=="NON - CRIMINAL"
df_crime = df_crime[mask]
# Convert floats to integers.
df_crime = df_crime.astype({"Primary Type":str, "Community Area":int, "Year":int})
# Group by crime types ("Primary Type"), count the number of "Year" in each crime type.
df_crime_chicago = df_crime.groupby("Primary Type").count()["Year"]
# Create a dataframe about community area/Chicago population.
# I need this because the above df_crime only has the number of case, which is
# uncomparable with other community areas. I will process this data to produce
# the numer of crimes per 1,000 people.
df_population = pd.read_csv("population_by_community_area.csv")
# Extract a value of Chicago's population.
chicago_population = df_population.loc[77, 'Population']

# Replace "the numbes of crimes" with "the number of crimes per 1,000 population"
df_crimerate_chicago = 1000*df_crime_chicago/chicago_population

# Create a datafram of other community areas and "concat" them with df_crimerate_chicago
# to create the full data. Of course, "the number of crimes" will be converted into
# "the number of crimes per 1,000 people" as with the above "df_crimerate_chicago".
for x in range(77):
    df_crime_communityarea = df_crime[df_crime["Community Area"]==x+1].groupby("Primary Type").count()["Year"]
    df_population_communityarea = df_population.loc[int(x),'Population']
    df_crimerate_communityarea = 1000*df_crime_communityarea/df_population_communityarea
    # Concat a community area dataframe with the Chicago dataframe, and fill the
    # box with "NA" with the value 0.
    df_crimerate_chicago = pd.concat([df_crimerate_chicago, df_crimerate_communityarea], axis=1).fillna(value=0)
    # Here, all the columns are named "Year".

# Rename the column names from "Year" to the number which corresponds with the order
# of community area numbers, so that I can sort them. I need to bring the first
# column (which is the data of Chicago overall) to the tail in order to match
# the order of them in the next file ("SelectedIndicators.csv").
# I know this looks stupid. I tried ".rename(columns{"Year": int(x)})" in
# the above for loop, but it somehow didn't work. All the column names were
# labeled as "0".
df_crimerate_chicago.columns = [77,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,\
    18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,\
    44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,\
    70,71,72,73,74,75,76]
# Sort the columns order, only to bring the first column to the tail.
df_crimerate_chicago = df_crimerate_chicago.reindex_axis(sorted(df_crimerate_chicago.columns), axis=1)
# Traspose the columns with the indices.
df_crimerate_chicago = df_crimerate_chicago.T


# Now the third file which contains some useful indicators. In thie file,
# the data was already "groupedby" by community areas.
# Read the csv file with certain columns, and fill the "NA"s with "0".
df_indicators = pd.read_csv("SelectedIndicators.csv", \
    usecols = ["Community Area Number", "COMMUNITY AREA NAME", \
               "PERCENT HOUSEHOLDS BELOW POVERTY", \
               "PERCENT AGED 25+ WITHOUT HIGH SCHOOL DIPLOMA"]).fillna(value=0)
# Convert the "Community Area Number"s from float to integer. Others will not be changed.
df_indicators = df_indicators.astype({"Community Area Number":int, "COMMUNITY AREA NAME":str, \
    "PERCENT HOUSEHOLDS BELOW POVERTY":float, "PERCENT AGED 25+ WITHOUT HIGH SCHOOL DIPLOMA":float})

# Concat these dataframes. Community areas will be indices.
df = pd.concat([df_indicators, df_crimerate_chicago], axis=1)
# Round the value to 2nd decimal point.
df = df.round(decimals=2)

# Output to the csv file named "processed_data.csv".
df.to_csv("processed_data.csv")
