from __future__ import absolute_import

from documents.models import Document

from .models import Index


def cleanup():
    for document in Document.objects.all():
        IndexInstanceNode.objects.delete_nodes_for(document=document)

    Index.objects.all().delete()
