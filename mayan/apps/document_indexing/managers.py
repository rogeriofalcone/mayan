from __future__ import absolute_import

import logging

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from metadata.classes import MetadataClass

from .settings import AVAILABLE_INDEXING_FUNCTIONS
from .signals import (create_node_instance, add_document_to_node_instance,
    remove_document_from_node_instance, delete_node_instance)

logger = logging.getLogger(__name__)


class IndexManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)

    def update_for(self, document):
        """
        Update or create all the index instances related to a document
        """
        warnings = []

        eval_dict = {}
        document_metadata_dict = dict([(metadata.metadata_type.name, metadata.value) for metadata in document.documentmetadata_set.all() if metadata.value])
        eval_dict['document'] = document
        eval_dict['metadata'] = MetadataClass(document_metadata_dict)

        # Only update indexes where the document type is found or that do not have any document type specified
        for index in self.get_query_set().filter(Q(enabled=True) & (Q(document_types=None) | Q(document_types=document.document_type))):
            try:
                index.template_root.evaluate(eval_dict, document)
            except Exception as exception:
                logger.warning('exception: %s' % exception)


class IndexInstanceNodeManager(models.Manager):
    def delete_nodes_for(self, document):
        """
        Delete all the index instances related to a document
        """
        for node_instance in document.indexinstancenode_set.all():
            self.cascade_document_remove(node_instance, document)

    def cascade_document_remove(self, node_instance, document):
        """
        Delete a documents reference from an index instance and call itself
        recusively deleting documents and empty index instances up to the
        root of the tree
        """
        if not node_instance.is_root_node():
            remove_document_from_node_instance.send(sender=node_instance, document=document)
            node_instance.documents.remove(document)
            if node_instance.documents.count() == 0 and node_instance.get_children().count() == 0:
                # if there are no more documents and no children, delete
                # node and check parent for the same conditions
                parent = node_instance.parent
                delete_node_instance.send(sender=node_instance)
                node_instance.delete()
                self.cascade_document_remove(parent, document)
