from __future__ import absolute_import

import logging

from django.contrib.auth.models import User, Group

from rest_framework import generics
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from documents.models import Document, DocumentType

from .serializers import DocumentSerializer, DocumentTypeSerializer, UserSerializer, GroupSerializer
from .permissions import HasAPIPermission

logger = logging.getLogger(__name__)


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'v0': reverse('api-version-0', request=request),
        'v1': reverse('api-version-1', request=request),
    })


#class APIBase(View):
#     def get(self, request):
#        return [
#            {'name': 'Version 0 Alpha', 'url': reverse('api-version-0')}
#        ]


#class Version_0(View):
#    def get(self, request):
#        return [
#            {'name': 'Resources', 'resources': ['document/<pk>']}
#        ]


@api_view(('GET',))
def version_0(request, format=None):
    return Response('This version has been deprecated and removed.')


@api_view(('GET',))
def version_1(request, format=None):
    return Response({
        'documents': reverse('document-list', request=request),
        'document-types': reverse('documenttype-list', request=request),
        'users': reverse('user-list', request=request),
        'groups': reverse('group-list', request=request),
    })


class MayanAPIView(object):
    permission_classes = (HasAPIPermission,)


class DocumentList(MayanAPIView, generics.ListCreateAPIView):
    model = Document
    serializer_class = DocumentSerializer


class DocumentDetail(MayanAPIView, generics.RetrieveUpdateDestroyAPIView):
    model = Document
    serializer_class = DocumentSerializer


class DocumentTypeList(MayanAPIView, generics.ListCreateAPIView):
    model = DocumentType
    serializer_class = DocumentTypeSerializer


class DocumentTypeDetail(MayanAPIView, generics.RetrieveUpdateDestroyAPIView):
    model = DocumentType
    serializer_class = DocumentTypeSerializer


class UserList(MayanAPIView, generics.ListCreateAPIView):
    model = User
    serializer_class = UserSerializer


class UserDetail(MayanAPIView, generics.RetrieveUpdateDestroyAPIView):
    model = User
    serializer_class = UserSerializer


class GroupList(MayanAPIView, generics.ListCreateAPIView):
    model = Group
    serializer_class = GroupSerializer


class GroupDetail(MayanAPIView, generics.RetrieveUpdateDestroyAPIView):
    model = Group
    serializer_class = GroupSerializer
