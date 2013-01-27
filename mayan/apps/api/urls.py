from __future__ import absolute_import

from django.conf.urls import patterns, url, include

from .views import (DocumentList, DocumentDetail, DocumentTypeList,
    DocumentTypeDetail, UserList, UserDetail, GroupList, GroupDetail)


urlpatterns = patterns('api.views',
    url(r'^$', 'api_root'),
    
    
    url(r'^v0/$', 'version_0', name='api-version-0'),
    
    
    url(r'^v1/$', 'version_1', name='api-version-1'),

    url(r'^v1/documents/$', DocumentList.as_view(), name='document-list'),
    url(r'^v1/documents/(?P<pk>[0-9]+)/$', DocumentDetail.as_view(), name='document-detail'),

    url(r'^v1/document-types/$', DocumentTypeList.as_view(), name='documenttype-list'),
    url(r'^v1/document-types/(?P<pk>[0-9]+)/$', DocumentTypeDetail.as_view(), name='documenttype-detail'),

    url(r'^v1/users/$', UserList.as_view(), name='user-list'),
    url(r'^v1/users/(?P<pk>[0-9]+)/$', UserDetail.as_view(), name='user-detail'),

    url(r'^v1/groups/$', GroupList.as_view(), name='group-list'),
    url(r'^v1/groups/(?P<pk>[0-9]+)/$', GroupDetail.as_view(), name='group-detail'),
)

urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework'))
)
