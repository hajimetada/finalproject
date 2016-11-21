import pandas as pd

df = pd.read_csv("chicagocrimes_slim.csv")

# Drop broken rows and extract data of 2015.
mask_beat = df["Beat"].str.contains("false|true")
mask_district = df["District"].str.contains("false|true")
mask_2015 = DF["Year"]==2015
df = df[~mask_beat][~mask_district][mask_2015]

# Extract the data of specific community area.
mask_communityarea = DF["Community Area"]==4
df_ca = DF[mask_communityarea][mask_2015].groupby("Primary Type").count()["Date"]

df_total = DF[mask_2015].groupby("Primary Type").count()["Date"]

# Concat two dataframes (one for a chosen community area, one for Chicago overall)
df = pd.concat([COMMUNITYAREA, TOTAL], axis=1)

# Create a table.
table_homi = df_concatted.to_html(float_format = "%.3f", classes = "table table-striped", index_names = False, index = False)
table = table.replace('style="text-align: right;"', "")
