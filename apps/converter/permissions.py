from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

namespace = PermissionNamespace('converter', _(u'Converter'))

PERMISSION_TRANSFORMATION_CREATE = Permission.objects.register(namespace, 'transformation_create', _(u'Create new transformations'))
PERMISSION_TRANSFORMATION_DELETE = Permission.objects.register(namespace, 'transformation_delete', _(u'Delete transformations'))
PERMISSION_TRANSFORMATION_EDIT = Permission.objects.register(namespace, 'transformation_edit', _(u'Edit transformations'))
PERMISSION_TRANSFORMATION_VIEW = Permission.objects.register(namespace, 'transformation_view', _(u'View transformations'))
