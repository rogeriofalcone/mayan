from __future__ import absolute_import

from navigation.classes import Link

from .classes import Statistic, StatisticNamespace
from .links import link_execute, link_namespace_details, link_namespace_list

Link.bind_links([StatisticNamespace], [link_namespace_details])
Link.bind_links([StatisticNamespace, 'namespace_list'], link_namespace_list, menu_name='secondary_menu')
Link.bind_links([Statistic], [link_execute])
