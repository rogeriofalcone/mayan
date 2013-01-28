from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.classes import Link

from .icons import (icon_checkout_list, icon_check_out_document, icon_check_in_document)
from .permissions import (PERMISSION_DOCUMENT_CHECKOUT, PERMISSION_DOCUMENT_CHECKIN, PERMISSION_DOCUMENT_CHECKIN_OVERRIDE)


def is_checked_out(context):
    return context['object'].is_checked_out()


def is_not_checked_out(context):
    return not context['object'].is_checked_out()


checkout_list = Link(text=_(u'checkouts'), view='checkout_list', icon=icon_checkout_list)
checkout_document = Link(text=_('check out document'), view='checkout_document', args='object.pk', condition=is_not_checked_out, permissions=[PERMISSION_DOCUMENT_CHECKOUT], icon=icon_check_out_document)
checkin_document = Link(text=_('check in document'), view='checkin_document', args='object.pk', condition=is_checked_out, permissions=[PERMISSION_DOCUMENT_CHECKIN, PERMISSION_DOCUMENT_CHECKIN_OVERRIDE], icon=icon_check_in_document)
checkout_info = Link(text=_('check in/out'), view='checkout_info', args='object.pk', children_views=['checkout_document', 'checkin_document'], permissions=[PERMISSION_DOCUMENT_CHECKIN, PERMISSION_DOCUMENT_CHECKIN_OVERRIDE, PERMISSION_DOCUMENT_CHECKOUT], icon=icon_checkout_list)
