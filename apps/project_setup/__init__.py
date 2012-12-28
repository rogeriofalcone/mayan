from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import register_top_menu

from .links import setup_menu_link

setup_link = register_top_menu('setup_menu', link=setup_menu_link, position=-2)
