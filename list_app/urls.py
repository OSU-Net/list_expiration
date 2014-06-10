
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^index/$', 'list_app.views.list_index'),
    url(r'^list_edit/$', 'list_app.views.submit_list_edit'), #should these last two urls have a trailing '/'?
    url(r'^onid_transition/$', 'list_app.views.onid_transition')
)
