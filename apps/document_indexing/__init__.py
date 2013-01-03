from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import (register_top_menu, register_sidebar_template,
    bind_links)

from maintenance.api import MaintenanceNamespace
from documents.models import Document
from project_setup.api import register_setup

from .models import (Index, IndexTemplateNode, IndexInstanceNode)
from .links import (index_setup, index_setup_list, index_setup_create, index_setup_edit, index_setup_delete, index_setup_view, index_setup_document_types, template_node_create, template_node_edit, template_node_delete, index_list, index_parent, document_index_list, rebuild_index_instances, link_menu)

register_top_menu('indexes', link_menu)

namespace = MaintenanceNamespace(_(u'indexes'))
namespace.create_tool(rebuild_index_instances)

register_sidebar_template(['index_instance_list'], 'indexing_help.html')

bind_links([IndexInstanceNode], [index_parent])

bind_links([Document], [document_index_list], menu_name='form_header')

register_setup(index_setup)

bind_links([Index, 'index_setup_list', 'index_setup_create', 'template_node_edit', 'template_node_delete'], [index_setup_list, index_setup_create], menu_name='secondary_menu')

bind_links([Index], [index_setup_edit, index_setup_delete, index_setup_view, index_setup_document_types])

bind_links([IndexTemplateNode], [template_node_create, template_node_edit, template_node_delete])
