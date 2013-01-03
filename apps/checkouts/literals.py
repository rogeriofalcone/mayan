from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .icons import icon_checkout_state_checkedout, icon_checkout_state_checkedin

STATE_CHECKED_OUT = 'checkedout'
STATE_CHECKED_IN = 'checkedin'

STATE_ICONS = {
    STATE_CHECKED_OUT: icon_checkout_state_checkedout,
    STATE_CHECKED_IN: icon_checkout_state_checkedin,
}

STATE_LABELS = {
    STATE_CHECKED_OUT: _(u'checked out'),
    STATE_CHECKED_IN: _(u'checked in/available'),
}
