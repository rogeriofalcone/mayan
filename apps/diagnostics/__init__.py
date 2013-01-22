from __future__ import absolute_import

from navigation.classes import Link

from .api import DiagnosticTool
from .links import diagnostic_list, diagnostic_execute

Link.bind_links(['diagnostic_list'], diagnostic_list, menu_name='secondary_menu')
Link.bind_links([DiagnosticTool], diagnostic_execute)
