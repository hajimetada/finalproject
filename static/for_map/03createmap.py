import folium
import pandas as pd, geopandas as gpd
from IPython.display import HTML


crime_df = pd.read_csv("02map.csv")
crime_df.dropna(inplace = True)

from shapely.geometry import Point
geometry = [Point(xy) for xy in zip(crime_df.Longitude, crime_df.Latitude)]
crime_coords = gpd.GeoDataFrame(crime_df, geometry=geometry)

chi_coords = (41.8781,-87.6298)

map = folium.Map(location=chi_coords, zoom_start=13)

folium.GeoJson(open("community_areas.geojson"),
            name='geojson'
            ).add_to(map)

for each in crime_coords.iterrows():
    folium.Marker([each[1]['Latitude'],each[1]['Longitude']]).add_to(map)

map.save("03homicidemap.html")
