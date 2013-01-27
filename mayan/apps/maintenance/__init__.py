from __future__ import absolute_import

from navigation.classes import Link

from .api import MaintenanceTool
from .links import maintenance_menu, maintenance_execute

Link.bind_links(['maintenance_menu'], maintenance_menu, menu_name='secondary_menu')
Link.bind_links([MaintenanceTool], maintenance_execute)
