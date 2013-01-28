from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .icons import icon_statistics, icon_namespace_details, icon_execute


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser


statistics_link = Link(text=_(u'statistics'), view='namespace_list', icon=icon_statistics, condition=is_superuser, children_view_regex=[r'statistics'])
link_namespace_list = Link(text=_(u'namespace list'), view='namespace_list', icon=icon_statistics, condition=is_superuser, children_view_regex=[r'statistics'])
link_namespace_details = Link(text=_(u'details'), view='namespace_details', args='resolved_object.id', icon=icon_namespace_details, condition=is_superuser)
link_execute = Link(text=_(u'execute'), view='execute', args='resolved_object.id', icon=icon_execute, condition=is_superuser)
