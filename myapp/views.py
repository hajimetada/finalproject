from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy


def home(request):
    return render(request, '01Chicago.html')

from .forms import InputForm
from .models import COMMUNITYAREA_DICT
# Provide a form to select a community area and redirect to the "portal", which
# collect outputs from other functions, convert them into variabvles, and send
# them to "02CommunityChecker.html".
def form(request):

    communityarea = request.POST.get('communityarea', '')
    # COMMUNITYAREA_DICT["F"] is empty. So users are firstly led to the final
    # line of thie function and provided the pull-down options first.
    if not communityarea: communityarea = request.GET.get('communityarea', 'F')

    params = {'form_action' : reverse_lazy('myapp:form'),
              'form_method' : 'get',
              'form' : InputForm({'communityarea' : communityarea}),
              'communityarea' : communityarea}

    if COMMUNITYAREA_DICT[communityarea]:
        # After choosing a community area, a user will be redirected to "portal".
        return HttpResponseRedirect(reverse_lazy('myapp:portal', kwargs={'communityarea': communityarea}))
    return render(request, '02CommunityChecker.html', params)



# This function collects outputs such as tables form other functions, convert them
# into variables, and send into the "02CommunityChecker.html".
def portal(request, communityarea):
    params = {"table_crime": reverse_lazy("myapp:table_crime", \
                                kwargs={'communityarea': communityarea}),
              "crimemap": reverse_lazy('myapp:crimemap', \
                                kwargs={'communityarea': communityarea}),
              "table_educ": reverse_lazy('myapp:table_educ', \
                                kwargs={'communityarea': communityarea}),
              "graph_educ": reverse_lazy('myapp:graph_educ',\
                                kwargs={'communityarea': communityarea}),
    }

    return render(request, '02CommunityChecker.html', params)



from os.path import join
from django.conf import settings
import pandas as pd
# Generate a table with some crime information about the community area and
# Chicago overall.
def table_crime(request, communityarea):

   filename = join(settings.STATIC_ROOT, "chicagocrimes_slim.csv")
   df = pd.read_csv(filename)

   # Read population of the community area and Chicago so that we can calculate
   # crime rate later.
   filename_pop = join(settings.STATIC_ROOT, "population_by_community_area.csv")
   df_population = pd.read_csv(filename_pop)
   #communityarea_index = communityarea-1)
   ca_pop = df_population.loc[int(communityarea)-1, 'Population']
   total_pop = df_population.loc[77,'Population']

   # Drop broken rows and extract data of 2015.
   mask_beat = df["Beat"].str.contains("false|true")
   mask_district = df["District"].str.contains("false|true")
   mask_2015 = df["Year"]==2015
   df = df[~mask_beat][~mask_district][mask_2015]

   # Extract the data of specific community area.
   mask_communityarea = df["Community Area"]==int(communityarea)
   df_ca = df[mask_communityarea][mask_2015].groupby("Primary Type").count()["Latitude"]
   df_total = df[mask_2015].groupby("Primary Type").count()["Longitude"]

   # The above dataframes only have number of crimes, so we need to calcualte
   # the crime rate.
   crimerate_ca = 1000*df_ca/int(ca_pop)
   crimerate_total = 1000*df_total/int(total_pop)

   # Concat two dataframes (one for a chosen community area, one for Chicago overall)
   df = pd.concat([crimerate_ca, crimerate_total], axis=1).rename(columns = {"Latitude": str(COMMUNITYAREA_DICT[communityarea]), "Longitude": "CHICAGO OVERALL"}).fillna(value=0)

   # Create a table.
   table = df.to_html(float_format = "%.3f", classes = "table table-striped", index_names = True, index = True)
   table = table.replace('style="text-align: right;"', "")

   return HttpResponse(table)


# Generate a table with some educational information about the community area and
# Chicago overall.
def table_educ(request, communityarea):

   filename = join(settings.STATIC_ROOT, "ERNESTO'S CSV")
   df = pd.read_csv(filename)

   # Create a mask
   mask = df["Community Area"].str.contains(str(communityarea) | "Total")

   # Create a table.
   table = df[mask].to_html(float_format = "%.3f", classes = "table table-striped", index_names = False, index = False)
   table = table.replace('style="text-align: right;"', "")

   return HttpResponse(table)


# Generate an educational trend graph about the community area and
# Chicago overall.
import matplotlib.pyplot as plt
def graph_educ(request, communityarea):
   filename = join(settings.STATIC_ROOT, "ERNESTO'S CSV")
   df = pd.read_csv(filename)

   # Plot the information about the community area.
   community_masked_df = df[df["Neighborhood"] == str(communityarea)][df["Year"] > 2010]
   X_community = community_masked_df["Year"].str
   Y_community = masked_df["educational attainment", df["Year"] == X]
   plt.figure()
   plt.plot(x = X_community, y = Y_community, color = "r")

   # Plot the information about Chicago overall.
   chicago_masked_df = df[df["Neighborhood"] == "Total"][df["Year"] > 2010]
   X_chicago = chicago_masked_df["Year"].str
   Y_chicago = masked_df["educational attainment", df["Year"] == X]
   plt.figure()
   plt.plot(x = X_chicago, y = Y_chicago, color = "b")

   # write bytes instead of file.
   from io import BytesIO
   figfile = BytesIO()

   figfile.seek(0)
   return HttpResponse(figfile.read(), content_type="image/png")


# Generate a map with some crime information about the community area.


import geopandas as gpd
def crimemap(request, commynityarea):
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

   located_crimes.rename(columns = {"community" : "communityarea"}, inplace = True)
   commu_df.rename(columns = {"community" : "communityarea"}, inplace = True)

   community_crimes = located_crimes[located_crimes['communityarea']== communityarea]
   community_boundaries = commu_df[commu_df['communityarea']== communityarea]

   base = community_boundaries.plot(color = "white")
   community_crimes.plot(ax = base)

   return HttpResponse(content_type="image/png")




def crimemap_view(request, communityarea):
   community_crimes = located_crimes[located_crimes['community']== communityarea]
   community_boundaries = commu_df[commu_df['community']== community]

   base = community_boundaries.plot(color = "white")
   community_crimes.plot(ax = base)
