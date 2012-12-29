from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.classes import Link

from .icons import icon_scheduler_tool_link
from .permissions import PERMISSION_VIEW_JOB_LIST

link_job_list = Link(text=_(u'interval job list'), view='job_list', permissions=[PERMISSION_VIEW_JOB_LIST], icon=icon_scheduler_tool_link)
