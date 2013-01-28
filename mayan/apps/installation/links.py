from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.classes import Link

from .icons import icon_installation_details
from .permissions import PERMISSION_INSTALLATION_DETAILS

installation_details = Link(text=_(u'installation details'), view='installation_details', permissions=[PERMISSION_INSTALLATION_DETAILS], icon=icon_installation_details)
