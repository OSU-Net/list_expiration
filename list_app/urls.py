
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^index', 'list_app.views.login_success'),
    url(r'^list_edit', 'list_app.views.list_edit'),
)
