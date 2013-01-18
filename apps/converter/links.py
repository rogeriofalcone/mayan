from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .icons import (icon_format_list, icon_transformation_create, icon_transformation_edit,
    icon_transformation_delete, icon_transformation_list)

from .permissions import (PERMISSION_TRANSFORMATION_CREATE, PERMISSION_TRANSFORMATION_DELETE,
    PERMISSION_TRANSFORMATION_EDIT, PERMISSION_TRANSFORMATION_VIEW)

def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser


link_formats_list = Link(text=_('file formats'), view='formats_list', icon=icon_format_list, condition=is_superuser, children_view_regex=[r'formats_list'])

link_transformation_list = Link(text=_(u'transformations'), view='transformation_list', args=['source.source_type', 'source.pk'], permissions=[PERMISSION_TRANSFORMATION_VIEW], icon=icon_transformation_list)
link_transformation_create = Link(text=_(u'add transformation'), view='transformation_create', args='source_object.gid', permissions=[PERMISSION_TRANSFORMATION_CREATE], icon=icon_transformation_create)
link_transformation_edit = Link(text=_(u'edit'), view='transformation_edit', args='object.pk', permissions=[PERMISSION_TRANSFORMATION_EDIT], icon=icon_transformation_edit)
link_transformation_delete = Link(text=_(u'delete'), view='transformation_delete', args='object.pk', permissions=[PERMISSION_TRANSFORMATION_DELETE], icon=icon_transformation_delete)
