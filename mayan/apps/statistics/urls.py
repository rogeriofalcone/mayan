from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('statistics.views',
    url(r'^$', 'statistics_list', (), 'statistics_list'),
    url(r'^namespace/(?P<namespace_id>\w+)/details/$', 'namespace_details', (), 'namespace_details'),
    url(r'^(?P<statistic_id>\w+)/execute/$', 'execute', (), 'execute'),
)
