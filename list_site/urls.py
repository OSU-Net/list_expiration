from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'list_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django_cas.views.login'),
    url(r'^accounts/logout/$', 'django_cas.views.logout'),
    url(r'^app/', include('list_app.urls',namespace='list_app')),
)
