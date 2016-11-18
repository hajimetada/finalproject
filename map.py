%matplotlib inline
import pandas as pd, geopandas as gpd

commu_df = gpd.read_file("community_areas.geojson")

from shapely.geometry import Point
crime_df = pd.read_csv("first_degree_murders.csv", usecols = [19, 20])
crime_df.dropna(inplace = True)
geometry = [Point(xy) for xy in zip(crime_df.Longitude, crime_df.Latitude)]

crime_coords = gpd.GeoDataFrame(crime_df, crs = commu_df.crs, geometry=geometry)

located_crimes = gpd.tools.sjoin(crime_coords, commu_df, how = 'left', op = 'within')

located_crimes.rename(columns = {"index_right" : "Murders"}, inplace = True)
murder_area_count = located_crimes.groupby("community").count()[["Murders"]]

mapped_murders = pd.merge(commu_df, murder_area_count, how = "inner", left_on = "community", right_index = True)
# ax = mapped_murders.plot(column = "Murders", k = 9, linewidth = 1)
base = commu_df.plot(color = "white")
crime_coords.plot(ax = base)
ax.set_axis_off()
