from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^lists/', include('list_app.urls', namespace='list_app')),
    url(r'^logout', 'django_cas.views.logout'),
    url(r'^login', 'django_cas.views.login'),
)
