from __future__ import absolute_import

import logging

from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from documents.models import Document
from maintenance.classes import MaintenanceNamespace
from metadata.models import DocumentMetadata
from navigation.api import register_top_menu, register_sidebar_template
from navigation.classes import Link
from project_setup.api import register_setup

from .links import (index_setup, index_setup_list, index_setup_create,
    index_setup_edit, index_setup_delete, index_setup_view, index_setup_document_types,
    template_node_create, template_node_edit, template_node_delete, index_list,
    index_parent, document_index_list, rebuild_index_instances, link_menu)
from .models import (Index, IndexTemplateNode, IndexInstanceNode)

logger = logging.getLogger(__name__)

namespace = MaintenanceNamespace(_(u'indexes'))
namespace.create_tool(rebuild_index_instances)

register_top_menu('indexes', link_menu)

register_sidebar_template(['index_instance_list'], 'indexing_help.html')

register_setup(index_setup)

Link.bind_links([IndexInstanceNode], [index_parent])
Link.bind_links([Document], [document_index_list], menu_name='form_header')
Link.bind_links([Index, 'index_setup_list', 'index_setup_create'], [index_setup_list, index_setup_create], menu_name='secondary_menu')
Link.bind_links([Index], [index_setup_edit, index_setup_delete, index_setup_view, index_setup_document_types])
Link.bind_links([IndexTemplateNode], [template_node_create, template_node_edit, template_node_delete])

@receiver(post_save, dispatch_uid='document_index_update', sender=Document)
def document_index_update(sender, **kwargs):
    logger.debug('document_index_update; %s' % kwargs)
    # TODO: save result in index log
    IndexInstanceNode.objects.delete_nodes_for(document=kwargs['instance'])
    Index.objects.update_for(document=kwargs['instance'])


@receiver(pre_delete, dispatch_uid='document_index_delete', sender=Document)
def document_index_delete(sender, **kwargs):
    logger.debug('document_index_delete; %s' % kwargs)
    # TODO: save result in index log
    IndexInstanceNode.objects.delete_nodes_for(document=kwargs['instance'])


@receiver(post_save, dispatch_uid='document_metadata_index_update', sender=DocumentMetadata)
def document_metadata_index_update(sender, **kwargs):
    logger.debug('document_metadata_index_update; %s' % kwargs)
    # TODO: save result in index log
    IndexInstanceNode.objects.delete_nodes_for(document=kwargs['instance'].document)
    Index.objects.update_for(document=kwargs['instance'].document)


@receiver(pre_delete, dispatch_uid='document_metadata_index_delete', sender=DocumentMetadata)
def document_metadata_index_delete(sender, **kwargs):
    logger.debug('document_metadata_index_delete; %s' % kwargs)
    # TODO: save result in index log
    IndexInstanceNode.objects.delete_nodes_for(document=kwargs['instance'].document)


@receiver(post_delete, dispatch_uid='document_metadata_index_post_delete', sender=DocumentMetadata)
def document_metadata_index_post_delete(sender, **kwargs):
    logger.debug('document_metadata_index_post_delete; %s' % kwargs)
    # TODO: save result in index log
    Index.objects.update_for(document=kwargs['instance'].document)
