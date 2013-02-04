from __future__ import absolute_import

from django.dispatch import receiver

from document_indexing.signals import (create_node_instance,
    add_document_to_node_instance, remove_document_from_node_instance,
    delete_node_instance)

from .classes import LocalFilesystem

local_filesystem_sharing = LocalFilesystem()


@receiver(create_node_instance, dispatch_uid='create_node')
def create_node(sender, **kwargs):
    print 'create folder: %s, kwargs: %s' % (sender, kwargs)
    local_filesystem_sharing.create_node(node_instance=kwargs['node_instance'])
    print 'post create folder'


@receiver(delete_node_instance, dispatch_uid='delete_node')
def delete_node(sender, **kwargs):
    local_filesystem_sharing.delete_node(node_instance=kwargs['node_instance'])
    print 'delete folder'



'''
@receiver(pre_delete, dispatch_uid='document_index_delete', sender=Document)
def document_index_delete(sender, **kwargs):
    # TODO: save result in index log
    IndexInstanceNode.objects.delete_nodes_for(document=kwargs['instance'])


@receiver(post_save, dispatch_uid='document_metadata_index_update', sender=DocumentMetadata)
def document_metadata_index_update(sender, **kwargs):
    # TODO: save result in index log
    IndexInstanceNode.objects.delete_nodes_for(document=kwargs['instance'].document)
    Index.objects.update_for(document=kwargs['instance'].document)


@receiver(pre_delete, dispatch_uid='document_metadata_index_delete', sender=DocumentMetadata)
def document_metadata_index_delete(sender, **kwargs):
    # TODO: save result in index log
    IndexInstanceNode.objects.delete_nodes_for(document=kwargs['instance'].document)


@receiver(post_delete, dispatch_uid='document_metadata_index_post_delete', sender=DocumentMetadata)
def document_metadata_index_post_delete(sender, **kwargs):
    # TODO: save result in index log
    Index.objects.update_for(document=kwargs['instance'].document)

create_node_instance = Signal(providing_args=['index_instance'])
add_document_to_node_instance = Signal(providing_args=['index_instance', 'document'])
remove_document_from_node_instance = Signal(providing_args=['index_instance', 'document'])
delete_node_instance = Signal(providing_args=['index_instance'])

'''

"""




                try:
                    fs_create_index_directory(index_instance)
                except Exception, exc:
                    warnings.append(_(u'Error updating document index, expression: %(expression)s; %(exception)s') % {
                        'expression': template_node.expression, 'exception': exc})

                    suffix = find_lowest_available_suffix(index_instance, document)
                    document_count = DocumentRenameCount(
                        index_instance_node=index_instance,
                        document=document,
                        suffix=suffix
                    )
                    document_count.save()

                    try:
                        fs_create_document_link(index_instance, document, suffix)
                    except Exception, exc:
                        warnings.append(_(u'Error updating document index, expression: %(expression)s; %(exception)s') % {
                            'expression': template_node.expression, 'exception': exc})


#delete
        document_rename_count = DocumentRenameCount.objects.get(index_instance_node=index_instance, document=document)
        fs_delete_document_link(index_instance, document, document_rename_count.suffix)
        document_rename_count.delete()
"""
