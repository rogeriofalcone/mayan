from __future__ import absolute_import

from rest_framework import generics
from taggit.models import Tag

from rest_api.filters import nucleosObjectPermissionsFilter
from rest_api.permissions import nucleosPermission

from .permissions import PERMISSION_TAG_VIEW
from .serializers import TagSerializer


class APITagView(generics.RetrieveAPIView):
    """
    Details of the selected tag.
    """
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    permission_classes = (nucleosPermission,)
    nucleos_object_permissions = {'GET': [PERMISSION_TAG_VIEW]}


class APITagListView(generics.ListAPIView):
    """
    Returns a list of all the tags.
    """

    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    filter_backends = (nucleosObjectPermissionsFilter,)
    nucleos_object_permissions = {'GET': [PERMISSION_TAG_VIEW]}
