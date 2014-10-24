
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^index/$', 'list_app.views.list_index', name='list_index'),
    url(r'^list_edit/$', 'list_app.views.submit_list_edit'), #should these last two urls have a trailing '/'?
    url(r'^onid_transition/$', 'list_app.views.onid_transition', name='onid_transition'),
    url(r'^no_onid/$', 'list_app.views.no_onid', name='no_onid'),
    url(r'^test_index/$', 'list_app.views.test_index', name='test_index'),
    url(r'^mailman_cas/(?P<list_name>\w+)$', 'django_cas.views.mm_authenticate'),
)
