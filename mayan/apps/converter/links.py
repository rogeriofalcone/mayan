from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .icons import (icon_format_list, icon_transformation_create, icon_transformation_edit,
    icon_transformation_delete, icon_transformation_list, icon_transformation_clear)

from .permissions import (PERMISSION_TRANSFORMATION_CREATE, PERMISSION_TRANSFORMATION_DELETE,
    PERMISSION_TRANSFORMATION_EDIT, PERMISSION_TRANSFORMATION_VIEW)


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser


def get_app_label(context):
    try:
        return context['source_object']._meta.app_label
    except KeyError:
        return context['resolved_object']._meta.app_label        


def get_module_name(context):
    try:
        return context['source_object']._meta.module_name
    except KeyError:
        return context['resolved_object']._meta.module_name        


link_formats_list = Link(text=_('file formats'), view='formats_list', icon=icon_format_list, condition=is_superuser, children_view_regex=[r'formats_list'])

link_transformation_list = Link(text=_(u'transformations'), view='transformation_list', args=[get_app_label, get_module_name, 'resolved_object.pk'], permissions=[PERMISSION_TRANSFORMATION_VIEW], icon=icon_transformation_list)
link_transformation_create = Link(text=_(u'add transformation'), view='transformation_create', args=[get_app_label, get_module_name, 'source_object.pk'], permissions=[PERMISSION_TRANSFORMATION_CREATE], icon=icon_transformation_create)
link_transformation_edit = Link(text=_(u'edit'), view='transformation_edit', args='object.pk', permissions=[PERMISSION_TRANSFORMATION_EDIT], icon=icon_transformation_edit)
link_transformation_delete = Link(text=_(u'delete'), view='transformation_delete', args='object.pk', permissions=[PERMISSION_TRANSFORMATION_DELETE], icon=icon_transformation_delete)
link_document_clear_transformations = Link(text=_(u'clear transformations'), view='document_clear_transformations', args='resolved_object.id', icon=icon_transformation_clear)
link_document_multiple_clear_transformations = Link(text=_(u'clear transformations'), view='document_multiple_clear_transformations', icon=icon_transformation_clear)
