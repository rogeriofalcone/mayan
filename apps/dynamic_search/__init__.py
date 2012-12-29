from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import register_sidebar_template, bind_links, register_top_menu

from .links import search, search_advanced, search_again

register_sidebar_template(['search', 'search_advanced'], 'search_help.html')

bind_links(['search', 'search_advanced', 'results'], [search, search_advanced], menu_name='form_header')
bind_links(['results'], [search_again], menu_name='sidebar')

register_sidebar_template(['search', 'search_advanced', 'results'], 'recent_searches.html')

register_top_menu('search', link=search)#, children_path_regex=[r'^search/'])
