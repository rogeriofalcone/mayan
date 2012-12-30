from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from acls.permissions import ACLS_VIEW_ACL
from navigation.classes import Link

from .icons import (icon_tag_list, icon_tag_create, icon_tag_attach, icon_tag_document_remove,
    icon_document_list, icon_tag_delete, icon_tag_edit, icon_tagged_item_list,
    icon_tag_acl_list)
from .permissions import (PERMISSION_TAG_CREATE, PERMISSION_TAG_ATTACH,
    PERMISSION_TAG_REMOVE, PERMISSION_TAG_DELETE, PERMISSION_TAG_EDIT,
    PERMISSION_TAG_VIEW)


tag_list = Link(text=_(u'tag list'), view='tag_list', icon=icon_tag_list)
tag_create = Link(text=_(u'create new tag'), view='tag_create', icon=icon_tag_create, permissions=[PERMISSION_TAG_CREATE])
tag_attach = Link(text=_(u'attach tag'), view='tag_attach', args='object.pk', icon=icon_tag_attach, permissions=[PERMISSION_TAG_ATTACH])
tag_multiple_attach = Link(text=_(u'attach tag'), view='tag_multiple_attach', icon=icon_tag_attach)
tag_document_remove = Link(text=_(u'remove'), view='tag_remove', args=['object.pk', 'document.pk'], icon=icon_tag_document_remove, permissions=[PERMISSION_TAG_REMOVE])
tag_document_remove_multiple = Link(text=_(u'remove'), view='tag_multiple_remove', args='document.pk', icon=icon_tag_document_remove, permissions=[PERMISSION_TAG_REMOVE])
tag_document_list = Link(text=_(u'tags'), view='document_tags', args='object.pk', icon=icon_document_list, permissions=[PERMISSION_TAG_REMOVE, PERMISSION_TAG_ATTACH], children_view_regex=['tag'])
tag_delete = Link(text=_(u'delete'), view='tag_delete', args='object.pk', icon=icon_tag_delete, permissions=[PERMISSION_TAG_DELETE])
tag_multiple_delete = Link(text=_(u'delete'), view='tag_multiple_delete', icon=icon_tag_delete, permissions=[PERMISSION_TAG_DELETE])
tag_edit = Link(text=_(u'edit'), view='tag_edit', args='object.pk', icon=icon_tag_edit, permissions=[PERMISSION_TAG_EDIT])
tag_tagged_item_list = Link(text=_(u'tagged documents'), view='tag_tagged_item_list', args='object.pk', icon=icon_tagged_item_list)
tag_acl_list = Link(text=_(u'ACLs'), view='tag_acl_list', args='object.pk', icon=icon_tag_acl_list, permissions=[ACLS_VIEW_ACL])
multiple_documents_selection_tag_remove = Link(text=_(u'remove tag'), view='multiple_documents_selection_tag_remove')
single_document_multiple_tag_remove = Link(text=_(u'remove tags'), view='single_document_multiple_tag_remove', args='document.id', permissions=[PERMISSION_TAG_REMOVE])

link_menu = Link(text=_(u'tags'), view='tag_list', icon=icon_tag_list, children_view_regex=[r'^tag_(list|create|delete|edit|tagged|acl)'])

