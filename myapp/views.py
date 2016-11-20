from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy


def home(request):
    return render(request, '01Chicago.html')

from .forms import InputForm
from .models import COMMUNITYAREA_DICT
# select communityarea and redirect to table_and_graph_function
def form(request):

    communityarea = request.POST.get('communityarea', '')
    if not communityarea: communityarea = request.GET.get('communityarea', 'F')

    params = {'form_action' : reverse_lazy('myapp:form'),
              'form_method' : 'get',
              'form' : InputForm({'communityarea' : communityarea}),
              'communityarea' : communityarea}

    if COMMUNITYAREA_DICT[communityarea]:
        return HttpResponseRedirect(reverse_lazy('myapp:portal', kwargs={'communityarea': communityarea}))
    return render(request, '02CommunityChecker.html', params)



def portal(request, communityarea):
    params = {"table_crime": reverse_lazy('myapp:table_crime', \
                                kwargs={'communityarea': communityarea}),
              "map_crime": reverse_lazy('myapp:map_crime', \
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
# Display the table of specific cryme types and other variables such as
# educational attainment. # Display trend graphs for other variables.
def table_crime(request, communityarea):

   filename = join(settings.STATIC_ROOT, "ERNESTO'S CSV")
   df = pd.read_csv(filename)

   # Create a mask
   mask_homi = df["Primary Type"].str.contains("HOMICIDE")
   mask_rape = df["Primary Type"].str.contains("RAPE")
   mask_robb = df["Primary Type"].str.contains("ROBBERY")

   # GROUPBY
   df_masked = df[mask_].groupby("communityarea").count("Primary Type")

   # Create a table.
   table_homi = df[mask_].to_html(float_format = "%.3f", classes = "table table-striped", index_names = False, index = False)
   table = table.replace('style="text-align: right;"', "")

   return HttpResponse



def table_educ(request, communityarea):

   filename = join(settings.STATIC_ROOT, "ERNESTO'S CSV")
   df = pd.read_csv(filename)

   # Create a mask
   mask_homi = df["Primary Type"].str.contains("HOMICIDE")
   mask_rape = df["Primary Type"].str.contains("RAPE")
   mask_robb = df["Primary Type"].str.contains("ROBBERY")

   # GROUPBY
   df_masked = df[mask_].groupby("communityarea").count("Primary Type")

   # Create a table.
   table_homi = df[mask_].to_html(float_format = "%.3f", classes = "table table-striped", index_names = False, index = False)
   table = table.replace('style="text-align: right;"', "")



import matplotlib.pyplot as plt
def graph_educ(request, communityarea):
   filename = join(settings.STATIC_ROOT, "ERNESTO'S CSV")
   df = pd.read_csv(filename)

   masked_df = df[df["Neighborhood"] == str(communityarea)][df["Year"] > 2010]
   X = masked_df["Year"].str
   Y = masked_df["educational attainment", df["Year"] == X]

   plt.figure() # needed, to avoid adding curves in plot
   plt.plot(x = X, y = Y, color = "b")

   # write bytes instead of file.
   from io import BytesIO
   figfile = BytesIO()

   # this is where the color is used.
   try: plt.savefig(figfile, format = 'png')
   except ValueError: raise Http404("No such color")

   figfile.seek(0) # rewind to beginning of file
   return HttpResponse(figfile.read(), content_type="image/png")



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
   # ax = mapped_murders.plot(column = "Murders", k = 9, linewidth = 1)
   base = commu_df.plot(color = "white")
   crime_coords.plot(ax = base)
   ax.set_axis_off()

def crimemap_view(request, communityarea):
   community_crimes = located_crimes[located_crimes['community']== communityarea]
   community_boundaries = commu_df[commu_df['community']== community]

   base = community_boundaries.plot(color = "white")
   community_crimes.plot(ax = base)
