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


from os.path import join
from django.conf import settings
import pandas as pd
# This function collects outputs such as tables form other functions, convert them
# into variables, and send into the "02CommunityChecker.html".
def portal(request, communityarea):
    # This function's role is to pass variables collected form other functions
    # into the template. However, somehow I was not able obtain a table as a
    # variavleto from another function, so I will generate a table in this function.

    params = {"crimetable": crimetable(request, communityarea),
              "crimemap": reverse_lazy('myapp:crimemap', \
                            kwargs={'communityarea': communityarea}),
              "graph_educ": reverse_lazy('myapp:graph_educ',\
                            kwargs={'communityarea': communityarea}),
              "graph_poverty": reverse_lazy('myapp:graph_poverty',\
                            kwargs={'communityarea': communityarea}),
             }

    return render(request, '02CommunityChecker.html', params)


def crimetable(request, communityarea):
    # Generate a table with all the crime information about the community area and
    # Chicago overall, and the rank of the community by crime type.
    filename = join(settings.STATIC_ROOT, "processed_data.csv")
    df = pd.read_csv(filename)
    # Create a mask to pull the data of designated community area and Chicago overall.
    mask = (df["Community Area Number"]==int(communityarea))|(df["Community Area Number"]==0)
    # Apply mask, set "Community Area Number" as index so that the gap between
    # index and community area number will be resolved (originally,
    # index = community area number - 1). Remove unnecessary first three indicators,
    # and traspose indices and columns for the sake of user experience (the original
    # table is going to be too wide.).
    df_result = df[mask].set_index("Community Area Number").ix[:,4:].T
    # Add a new column for entering rank.
    df_result["Rank(Higher=Safer)/77"] = ""
    # Do the same manipulation as "df_result". This dataframe is necessary for
    # measuring ranks, so the data of Chicago needs to be dropped (index of Chicago is 0).
    df = df.set_index("Community Area Number").ix[:,4:].drop(0, axis=0)

    # Create a list of crime types.
    ctype = list(df.columns.values)
    # Create a for loop to obtain ranks of particular community area in all the
    # crime types, and add them to the rank cell in df_result.
    for x in ctype:
        df_ctype = df.rank(method='first').astype(int)
        a = df_ctype.loc[int(communityarea), str(x)]
        df_result.set_value(str(x), "Rank(Higher=Safer)/77", a)
    # Rename the columns.
    df_result = df_result.rename(columns={int(communityarea):COMMUNITYAREA_DICT[communityarea], 0:"CHICAGO"})
    # Create a table as a string.
    return df_result.to_html(float_format = "%.3f", classes = "table table-striped", index_names = True, index = True).replace('style="text-align: right;"', "")



# Generate a graph of educational indicator, which is % aged 25+ without
# highschool diploma.
import matplotlib.pyplot as plt
def graph_educ(request, communityarea):
   filename = join(settings.STATIC_ROOT, "processed_data.csv")
   df = pd.read_csv(filename)
   # Extract a few columns which are necessary.
   df = df[["Community Area Number", "COMMUNITY AREA NAME","PERCENT AGED 25+ WITHOUT HIGH SCHOOL DIPLOMA"]]
   DF = df.plot(kind="bar", x="COMMUNITY AREA NAME", y="PERCENT AGED 25+ WITHOUT HIGH SCHOOL DIPLOMA")
   # Lower the bottom of the figure so that it can accommodate x-labels.
   plt.subplots_adjust(bottom=.3)
   # Highlight the chosen community area and Chicago overall.
   DF.patches[int(communityarea)-1].set_color('r')
   DF.patches[77].set_color('r')
   # Write to bytes.
   from io import BytesIO
   figfile = BytesIO()
   fig = DF.get_figure()
   # Adjust the width and height of the figure.
   fig.set_size_inches(16, 6)
   # Cut off unnecessary margin and save the figure.
   fig.savefig(figfile, format="png", bbox_inches='tight')
   figfile.seek(0)
   return HttpResponse(figfile.read(), content_type="image/png")



# Generate a graph of educational indicator, which is % aged 25+ without
# highschool diploma.
def graph_poverty(request, communityarea):
   filename = join(settings.STATIC_ROOT, "processed_data.csv")
   df = pd.read_csv(filename)
   # Extract a few columns which are necessary.
   df = df[["Community Area Number", "COMMUNITY AREA NAME","PERCENT HOUSEHOLDS BELOW POVERTY"]]
   DF = df.plot(kind="bar", x="COMMUNITY AREA NAME", y="PERCENT HOUSEHOLDS BELOW POVERTY")
   # Lower the bottom of the figure so that it can accommodate x-labels.
   plt.subplots_adjust(bottom=.3)
   # Highlight the chosen community area and Chicago overall.
   DF.patches[int(communityarea)-1].set_color('r')
   DF.patches[77].set_color('r')
   # Write to bytes.
   from io import BytesIO
   figfile = BytesIO()
   fig = DF.get_figure()
   # Adjust the width and height of the figure.
   fig.set_size_inches(16, 6)
   # Cut off unnecessary margin and save the figure.
   fig.savefig(figfile, format="png", bbox_inches='tight')
   figfile.seek(0)
   return HttpResponse(figfile.read(), content_type="image/png")
