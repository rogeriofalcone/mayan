from __future__ import absolute_import

from documents.models import Document

from .models import Index, IndexInstanceNode


def do_rebuild_all_indexes():
    for document in Document.objects.all():
        IndexInstanceNode.objects.delete_nodes_for(document=document)
        Index.objects.update_for(document=document)
