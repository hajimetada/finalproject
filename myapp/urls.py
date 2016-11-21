from django.conf.urls import url

from . import views

app_name = 'myapp'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^form/$', views.form, name='form'),
    url(r'^portal/(?P<communityarea>[0-9\- ]+)/$', views.portal, name="portal"),
    url(r'^table_crime/(?P<communityarea>[0-9\- ]+)/$', views.table_crime, name="table_crime"),
    url(r'^crimemap/(?P<communityarea>[0-9\- ]+)/$', views.crimemap, name="crimemap"),
    url(r'^table_educ/(?P<communityarea>[0-9\- ]+)/$', views.table_educ, name="table_educ"),
    url(r'^graph_educ/(?P<communityarea>[0-9\- ]+)/$', views.graph_educ, name="graph_educ")
]
