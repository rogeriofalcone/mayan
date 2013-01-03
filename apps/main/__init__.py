from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from navigation.api import register_top_menu
from project_setup.api import register_setup
from project_tools.api import register_tool

from .conf.settings import SIDE_BAR_SEARCH, DISABLE_HOME_VIEW
from .links import (statistics, diagnostics, home_link)

__author__ = 'Roberto Rosario'
__copyright__ = 'Copyright 2011, 2012, 2013 Roberto Rosario'
__credits__ = ['Roberto Rosario',]
__license__ = 'GPL'
__maintainer__ = 'Roberto Rosario'
__email__ = 'roberto.rosario.gonzalez@gmail.com'
__status__ = 'Production'

__version_info__ = {
    'major': 1,
    'minor': 0,
    'micro': 0,
    'releaselevel': 'alpha',
    'serial': 0
}

if not DISABLE_HOME_VIEW:
    register_top_menu('home', link=home_link, position=0)


def get_version():
    '''
    Return the formatted version information
    '''
    vers = ['%(major)i.%(minor)i' % __version_info__, ]

    if __version_info__['micro']:
        vers.append('.%(micro)i' % __version_info__)
    if __version_info__['releaselevel'] != 'final':
        vers.append('%(releaselevel)s%(serial)i' % __version_info__)
    return ''.join(vers)


__version__ = get_version()


#register_tool(statistics)
#register_tool(diagnostics)

