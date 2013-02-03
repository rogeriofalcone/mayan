from __future__ import absolute_import

from acls.api import class_permissions
from acls.permissions import ACLS_VIEW_ACL, ACLS_EDIT_ACL
from documents.models import Document
from navigation.classes import Link

from .links import acl_list
from acls.links import link_acl_list

Link.bind_links([Document], [link_acl_list], menu_name='form_header')

class_permissions(Document, [
    ACLS_VIEW_ACL,
    ACLS_EDIT_ACL
])
