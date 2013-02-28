from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .icons import icon_document_acls

from acls.permissions import ACLS_VIEW_ACL
from navigation.classes import Link

link_acl_list = Link(text=_(u'ACLs'), view='document_acl_list', args='resolved_object.pk', permissions=[ACLS_VIEW_ACL], icon=icon_document_acls)
