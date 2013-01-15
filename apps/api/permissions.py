from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import PermissionDenied

from rest_framework.permissions import BasePermission

from permissions.models import PermissionNamespace, Permission


class HasAPIPermission(BasePermission):
    """
    Allows only users with the API access permission
    """

    def has_permission(self, request, view, obj=None):
        try:
            Permission.objects.check_permissions(request.user, [PERMISSION_API_ACCESS])
        except PermissionDenied:
            return False
        else:
            return True


namespace = PermissionNamespace('api', _(u'API'))

PERMISSION_API_ACCESS = Permission.objects.register(namespace, 'api_access', _(u'Access the API'))
