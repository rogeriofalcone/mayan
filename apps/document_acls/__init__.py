from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from documents.models import Document
from navigation.api import bind_links
from acls.api import class_permissions
from acls.permissions import ACLS_VIEW_ACL, ACLS_EDIT_ACL

from .links import acl_list

bind_links([Document], [acl_list], menu_name='form_header')

class_permissions(Document, [
    ACLS_VIEW_ACL,
    ACLS_EDIT_ACL
])
