# I'm going to integrate three files ("Crimes_-_2001_to_present.csv",
# "population_by_community_area.csv", and "SelectedIndicators.csv") into one
# file ("processed_data.csv").


import pandas as pd
# This file is from City of Chicago Data Portal.
df_crime = pd.read_csv("Crimes_-_2001_to_present.csv")
# Extract a few variables that are necessary to this webapp.
df_crime = df_crime[["Primary Type", "Community Area", "Year", "Latitude", "Longitude"]]
# Extract the data of 2015. 2015 is the latest data which is complete (2016 is still ongoing),
# and drop rows with missing values.
df_crime = df_crime[df_crime["Year"]==2015].dropna()
# Pick up only HOMICIDES due to the speed purpose. If I pick up more crime types,
# the webapp will crauh.
df_crime = df_crime[df_crime["Primary Type"]=="HOMICIDE"]
# Convert floats to integers.
df_crime = df_crime.astype({"Primary Type":str, "Community Area":int, "Year":int, "Latitude":float, "Longitude":float})


# Output to the csv file named "processed_data.csv".
df_crime.to_csv("homicidedata_for_map.csv")
