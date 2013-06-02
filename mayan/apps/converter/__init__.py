from __future__ import absolute_import

from django.core.exceptions import ImproperlyConfigured

from acls.api import class_permissions
from documents.models import Document, DocumentPage
from navigation.api import register_multi_item_links, register_sidebar_template
from navigation.classes import Link
from project_tools.api import register_tool

from .links import (link_formats_list, link_transformation_list,
    link_transformation_create, link_transformation_edit, link_transformation_delete,
    link_document_clear_transformations, link_document_multiple_clear_transformations)
from .models import Transformation
from .permissions import (PERMISSION_TRANSFORMATION_CREATE, PERMISSION_TRANSFORMATION_DELETE,
    PERMISSION_TRANSFORMATION_EDIT, PERMISSION_TRANSFORMATION_VIEW)

register_sidebar_template(['formats_list'], 'converter_file_formats_help.html')

Link.bind_links(['transformation_create', 'transformation_list', 'transformation_edit', 'transformation_delete'], [link_transformation_create], menu_name='sidebar')
Link.bind_links([Transformation], [link_transformation_edit, link_transformation_delete])

register_tool(link_formats_list)

# Register document links
Link.bind_links([Document], [link_document_clear_transformations])
register_multi_item_links(['document_find_duplicates', 'folder_view', 'index_instance_node_view', 'document_type_document_list', 'search', 'results', 'document_group_view', 'document_list', 'document_list_recent', 'tag_tagged_item_list'], [link_document_multiple_clear_transformations])

Link.bind_links([DocumentPage], [link_transformation_list])

class_permissions(Document, [
    PERMISSION_TRANSFORMATION_CREATE, PERMISSION_TRANSFORMATION_DELETE,
    PERMISSION_TRANSFORMATION_EDIT, PERMISSION_TRANSFORMATION_VIEW,
])
