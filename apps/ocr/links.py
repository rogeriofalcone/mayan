from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.classes import Link

from .icons import icon_submit_document, icon_ocr_cleanup
from .permissions import (PERMISSION_OCR_DOCUMENT,
    PERMISSION_OCR_DOCUMENT_DELETE, PERMISSION_OCR_QUEUE_ENABLE_DISABLE,
    PERMISSION_OCR_CLEAN_ALL_PAGES)

re_queue_document = Link(text=_('re-queue'), view='re_queue_document', args='object.id', permissions=[PERMISSION_OCR_DOCUMENT])
re_queue_multiple_document = Link(text=_('re-queue'), view='re_queue_multiple_document', permissions=[PERMISSION_OCR_DOCUMENT])
queue_document_delete = Link(text=_(u'delete'), view='queue_document_delete', args='object.id', permissions=[PERMISSION_OCR_DOCUMENT_DELETE])
queue_document_multiple_delete = Link(text=_(u'delete'), view='queue_document_multiple_delete', permissions=[PERMISSION_OCR_DOCUMENT_DELETE])

document_queue_disable = Link(text=_(u'stop queue'), view='document_queue_disable', args='queue.id', permissions=[PERMISSION_OCR_QUEUE_ENABLE_DISABLE])
document_queue_enable = Link(text=_(u'activate queue'), view='document_queue_enable', args='queue.id', permissions=[PERMISSION_OCR_QUEUE_ENABLE_DISABLE])

queue_document_list = Link(text=_(u'queue document list'), view='queue_document_list', permissions=[PERMISSION_OCR_DOCUMENT])
ocr_tool_link = Link(text=_(u'OCR'), view='queue_document_list', icon=icon_submit_document, permissions=[PERMISSION_OCR_DOCUMENT], children_view_regex=[r'queue_', r'document_queue'])

setup_queue_transformation_list = Link(text=_(u'transformations'), view='setup_queue_transformation_list', args='queue.pk')
setup_queue_transformation_create = Link(text=_(u'add transformation'), view='setup_queue_transformation_create', args='queue.pk')
setup_queue_transformation_edit = Link(text=_(u'edit'), view='setup_queue_transformation_edit', args='transformation.pk')
setup_queue_transformation_delete = Link(text=_(u'delete'), view='setup_queue_transformation_delete', args='transformation.pk')

submit_document = Link(text=_('submit to OCR queue'), view='submit_document', args='object.id', icon=icon_submit_document, permissions=[PERMISSION_OCR_DOCUMENT])
submit_document_multiple = Link(text=_('submit to OCR queue'), view='submit_document_multiple', icon=icon_submit_document, permissions=[PERMISSION_OCR_DOCUMENT])

all_document_ocr_cleanup = Link(text=_(u'clean up pages content'), view='all_document_ocr_cleanup', icon=icon_ocr_cleanup, permissions=[PERMISSION_OCR_CLEAN_ALL_PAGES], description=_(u'Runs a language filter to remove common OCR mistakes from document pages content.'))
