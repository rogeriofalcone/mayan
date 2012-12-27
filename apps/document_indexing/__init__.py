from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import (register_top_menu, register_sidebar_template,
    register_links)

from main.api import register_maintenance_links
from documents.models import Document
from project_setup.api import register_setup

from .models import (Index, IndexTemplateNode, IndexInstanceNode)
from .links import (index_setup, index_setup_list, index_setup_create, index_setup_edit, index_setup_delete, index_setup_view, index_setup_document_types, template_node_create, template_node_edit, template_node_delete, index_list, index_parent, document_index_list, rebuild_index_instances, index_menu_link)

register_top_menu('indexes', index_menu_link)

register_maintenance_links([rebuild_index_instances], namespace='document_indexing', title=_(u'Indexes'))

register_sidebar_template(['index_instance_list'], 'indexing_help.html')

register_links(IndexInstanceNode, [index_parent])

register_links(Document, [document_index_list], menu_name='form_header')

register_setup(index_setup)

register_links([Index, 'index_setup_list', 'index_setup_create', 'template_node_edit', 'template_node_delete'], [index_setup_list, index_setup_create], menu_name='secondary_menu')

register_links(Index, [index_setup_edit, index_setup_delete, index_setup_view, index_setup_document_types])

register_links(IndexTemplateNode, [template_node_create, template_node_edit, template_node_delete])
