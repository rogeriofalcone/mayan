from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _

from document_indexing.models import IndexInstanceNode
from documents.models import Document


class FSDocumentRenameCount(models.Model):
    index_instance_node = models.ForeignKey(IndexInstanceNode, verbose_name=_(u'index instance'))
    document = models.ForeignKey(Document, verbose_name=_(u'document'))
    suffix = models.PositiveIntegerField(blank=True, verbose_name=(u'suffix'))

    def __unicode__(self):
        return u'%s - %s - %s' % (self.index_instance_node, self.document, self.suffix or u'0')

    class Meta:
        verbose_name = _(u'filesystem document rename count')
        verbose_name_plural = _(u'filesystem documents rename count')
