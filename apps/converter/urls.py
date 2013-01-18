from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('converter.views',
    url(r'^formats/$', 'formats_list', (), 'formats_list'),

    url(r'^source/(?P<source_gid>[.\w]+)/$', 'transformation_create', (), 'transformation_create'),
    url(r'^transformation/(?P<transformation_pk>\d+)/edit/$', 'transformation_edit', (), 'transformation_edit'),
    url(r'^transformation/(?P<transformation_pk>\d+)/delete/$', 'transformation_delete', (), 'transformation_delete'),
)
