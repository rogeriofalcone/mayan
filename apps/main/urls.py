from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('main.views',
    url(r'^$', 'home', (), 'home'),
    url(r'^statistics/$', 'statistics', (), 'statistics'),
)
