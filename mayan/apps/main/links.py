from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.classes import Link

from .icons import icon_home

def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser


statistics = Link(text=_(u'statistics'), view='statistics', condition=is_superuser)#'famfam': 'table', 'icon': 'blackboard_sum.png', , 'children_view_regex': [r'statistics']}
home_link = Link(text=_(u'home'), view='home', icon=icon_home)
