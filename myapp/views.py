from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy


from .forms import InputForm
from .models import NEIGHBORHOOD_DICT
# select neighborhood and redirect to table_and_graph_function
def form(request):

    neighborhood = request.POST.get('neighborhood', '')
    if not yvar: yvar = request.GET.get('neighborhood', 'F')

    params = {'form_action' : reverse_lazy('myapp:form'),
              'form_method' : 'get',
              'form' : InputForm({'neighborhood' : neighborhood}),
              'neighborhood' : NEIGHBODHOOD_DICT[neighborhood]}

    if NEIGHBORHOOD_DICT[neighborhood]:
        return HttpResponseRedirect(reverse_lazy('myapp:table_and_graph', kwargs={'neighboorhood': neighborhood}))
    return render(request, 'form.html', params)


from os.path import join
from django.conf import settings
import pandas as pd
# Display the table of specific cryme types and other variables such as
# educational attainment. # Display trend graphs for other variables.
def table_and_graph(request, neighborhood):

   filename = join(settings.STATIC_ROOT, "ERNESTO'S CSV")
   df = pd.read_csv(filename)

   # Create a mask
   mask_homi = df["Primary Type"].str.contains("HOMICIDE")
   mask_rape = df["Primary Type"].str.contains("RAPE")
   mask_robb = df["Primary Type"].str.contains("ROBBERY")

   # GROUPBY
   df_masked = df[mask_].groupby("neighborhood").count("Primary Type")



   # Create a table.
   table_homi = df[mask_].to_html(float_format = "%.3f", classes = "table table-striped", index_names = False, index = False)
   table = table.replace('style="text-align: right;"', "")

   return render(request, "JUAN'S HTML",
                {"title": "Is "+NEIGHBORFOOD+" A Good Place to Live?",
                 "table_crime1": table_crime1, # A table of the neighborhood, the city average, and the rank?.
                 "table_crime2": table_crime2, # Same here.
                 "table_crime3": table_crime3, # Same here.
                 "table_other1": table_other1,
                 "table_other2": table_other2}) # Same here.

   return render(request, "JUAN'S HTML", {"table_title" : "An astounding plot!",
        "pic_source" : reverse_lazy("myapp:pic",
                                    kwargs = {'neighborhood' : neighborhood})})





import matplotlib.pyplot as plt
def pic(request, neighborhood):
   masked_df = df[df["Neighborhood"] == str(neigborhood)]
   X = masked_df["Year"].str
   Y = masked_df["educational attainment", df["Year"] == X]

   plt.figure() # needed, to avoid adding curves in plot
   plt.plot(x = X, y = Y, color = "b")

   # write bytes instead of file.
   from io import BytesIO
   figfile = BytesIO()

   # this is where the color is used.
   try: plt.savefig(figfile, format = 'png')
   # except ValueError: raise Http404("No such color")

   figfile.seek(0) # rewind to beginning of file
   return HttpResponse(figfile.read(), content_type="image/png")
