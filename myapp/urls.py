from django.conf.urls import url

from . import views

app_name = 'myapp'
urlpatterns = [

    url(r'^$', views.form, name='form'),
    url(r'^(?P<communityarea>[A-Za-z\- ]+)/$', views.table_and_graph, name="table_and_graph"),
    url(r'^pic/(?P<communityarea>[A-Za-z\- ]+)/$', views.pib, name="pic")
]
