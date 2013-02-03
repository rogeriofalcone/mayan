from __future__ import absolute_import

import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db import transaction

from converter.literals import DIMENSION_SEPARATOR
from converter.models import Transformation
from documents.models import Document
from documents.events import history_document_created
from metadata.api import save_metadata_list
from scheduler.api import register_interval_job, remove_job
from acls.utils import apply_default_acls

from .literals import (SOURCE_CHOICES, SOURCE_CHOICES_PLURAL,
    SOURCE_INTERACTIVE_UNCOMPRESS_CHOICES, SOURCE_CHOICE_WEB_FORM,
    SOURCE_CHOICE_STAGING, SOURCE_ICON_DISK, SOURCE_ICON_DRIVE,
    SOURCE_ICON_CHOICES, SOURCE_CHOICE_WATCH, SOURCE_UNCOMPRESS_CHOICES,
    SOURCE_UNCOMPRESS_CHOICE_Y)
from .compressed_file import CompressedFile, NotACompressedFile
from .staging import StagingFile

logger = logging.getLogger(__name__)


class BaseModel(models.Model):
    title = models.CharField(max_length=64, verbose_name=_(u'title'))
    enabled = models.BooleanField(default=True, verbose_name=_(u'enabled'))
    whitelist = models.TextField(blank=True, verbose_name=_(u'whitelist'), editable=False)
    blacklist = models.TextField(blank=True, verbose_name=_(u'blacklist'), editable=False)
    #document_type = models.ForeignKey(DocumentType, blank=True, null=True, verbose_name=_(u'document type'), help_text=(u'Optional document type to be applied to documents uploaded from this source.'))

    @classmethod
    def class_fullname(cls):
        return unicode(dict(SOURCE_CHOICES).get(cls.source_type))

    @classmethod
    def class_fullname_plural(cls):
        return unicode(dict(SOURCE_CHOICES_PLURAL).get(cls.source_type))

    def __unicode__(self):
        return u'%s' % self.title

    def fullname(self):
        return u' '.join([self.class_fullname(), '"%s"' % self.title])

    def internal_name(self):
        return u'%s_%d' % (self.source_type, self.pk)

    def get_transformation_list(self):
        return Transformation.objects.get_for_object_as_list(self)

    def upload_file(self, file_object, filename=None, use_file_name=False, document_type=None, expand=False, metadata_dict_list=None, user=None, document=None, new_version_data=None, command_line=False):
        is_compressed = None

        if expand:
            try:
                cf = CompressedFile(file_object)
                count = 1
                for fp in cf.children():
                    if command_line:
                        print 'Uploading file #%d: %s' % (count, fp)
                    self.upload_single_file(file_object=fp, filename=None, document_type=document_type, metadata_dict_list=metadata_dict_list, user=user)
                    fp.close()
                    count += 1

            except NotACompressedFile:
                is_compressed = False
                logging.debug('Exception: NotACompressedFile')
                if command_line:
                    raise
                self.upload_single_file(file_object=file_object, filename=filename, document_type=document_type, metadata_dict_list=metadata_dict_list, user=user)
            else:
                is_compressed = True
        else:
            self.upload_single_file(file_object, filename, use_file_name, document_type, metadata_dict_list, user, document, new_version_data)

        file_object.close()
        return {'is_compressed': is_compressed}

    @transaction.commit_on_success
    def upload_single_file(self, file_object, filename=None, use_file_name=False, document_type=None, metadata_dict_list=None, user=None, document=None, new_version_data=None):
        new_document = not document

        if not document:
            document = Document()
            if document_type:
                document.document_type = document_type
            document.save()

            apply_default_acls(document, user)

            if user:
                document.add_as_recent_document_for_user(user)
                history_document_created.commit(source_object=document, data={'user': user})
            else:
                history_document_created.commit(source_object=document)
        else:
            if use_file_name:
                filename = None
            else:
                filename = filename if filename else document.latest_version.filename

        if not new_version_data:
            new_version_data = {}

        try:
            new_version = document.new_version(file=file_object, user=user, **new_version_data)
        except Exception:
            # Don't leave the database in a broken state
            # document.delete()
            transaction.rollback()
            raise

        if filename:
            document.rename(filename)

        for document_page in new_version.pages.all():
            Transformation.objects.clone(self, document_page)

        #TODO: new HISTORY for version updates

        if metadata_dict_list and new_document:
            # Only do for new documents
            save_metadata_list(metadata_dict_list, document, create=True)

    class Meta:
        ordering = ('title',)
        abstract = True


class InteractiveBaseModel(BaseModel):
    icon = models.CharField(blank=True, null=True, max_length=24, choices=SOURCE_ICON_CHOICES, verbose_name=_(u'icon'), help_text=_(u'An icon to visually distinguish this source.'))

    def save(self, *args, **kwargs):
        if not self.icon:
            self.icon = self.default_icon
        super(BaseModel, self).save(*args, **kwargs)

    class Meta(BaseModel.Meta):
        abstract = True


class StagingFolder(InteractiveBaseModel):
    is_interactive = True
    source_type = SOURCE_CHOICE_STAGING
    default_icon = SOURCE_ICON_DRIVE

    folder_path = models.CharField(max_length=255, verbose_name=_(u'folder path'), help_text=_(u'Server side filesystem path.'))
    preview_width = models.IntegerField(verbose_name=_(u'preview width'), help_text=_(u'Width value to be passed to the converter backend.'))
    preview_height = models.IntegerField(blank=True, null=True, verbose_name=_(u'preview height'), help_text=_(u'Height value to be passed to the converter backend.'))
    uncompress = models.CharField(max_length=1, choices=SOURCE_INTERACTIVE_UNCOMPRESS_CHOICES, verbose_name=_(u'uncompress'), help_text=_(u'Whether to expand or not compressed archives.'))
    delete_after_upload = models.BooleanField(default=True, verbose_name=_(u'delete after upload'), help_text=_(u'Delete the file after is has been successfully uploaded.'))

    def get_preview_size(self):
        dimensions = []
        dimensions.append(unicode(self.preview_width))
        if self.preview_height:
            dimensions.append(unicode(self.preview_height))

        return DIMENSION_SEPARATOR.join(dimensions)

    def create_staging_file_class(self):
        cls = type('StagingFile', (StagingFile,), dict(StagingFile.__dict__))
        cls.set_path(self.folder_path)
        cls.set_source(self)
        return cls

    class Meta(InteractiveBaseModel.Meta):
        verbose_name = _(u'staging folder')
        verbose_name_plural = _(u'staging folders')

"""
class SourceMetadata(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    metadata_type = models.ForeignKey(MetadataType, verbose_name=_(u'metadata type'))
    value = models.CharField(max_length=256, blank=True, verbose_name=_(u'value'))

    def __unicode__(self):
        return self.source

    class Meta:
        verbose_name = _(u'source metadata')
        verbose_name_plural = _(u'sources metadata')
"""


class WebForm(InteractiveBaseModel):
    is_interactive = True
    source_type = SOURCE_CHOICE_WEB_FORM
    default_icon = SOURCE_ICON_DISK

    uncompress = models.CharField(max_length=1, choices=SOURCE_INTERACTIVE_UNCOMPRESS_CHOICES, verbose_name=_(u'uncompress'), help_text=_(u'Whether to expand or not compressed archives.'))
    #Default path

    class Meta(InteractiveBaseModel.Meta):
        verbose_name = _(u'web form')
        verbose_name_plural = _(u'web forms')


class WatchFolder(BaseModel):
    is_interactive = False
    source_type = SOURCE_CHOICE_WATCH

    folder_path = models.CharField(max_length=255, verbose_name=_(u'folder path'), help_text=_(u'Server side filesystem path.'))
    uncompress = models.CharField(max_length=1, choices=SOURCE_UNCOMPRESS_CHOICES, verbose_name=_(u'uncompress'), help_text=_(u'Whether to expand or not compressed archives.'))
    delete_after_upload = models.BooleanField(default=True, verbose_name=_(u'delete after upload'), help_text=_(u'Delete the file after is has been successfully uploaded.'))
    interval = models.PositiveIntegerField(verbose_name=_(u'interval'), help_text=_(u'Inverval in seconds where the watch folder path is checked for new documents.'))

    def save(self, *args, **kwargs):
        if self.pk:
            remove_job(self.internal_name())
        super(WatchFolder, self).save(*args, **kwargs)
        self.schedule()

    def schedule(self):
        if self.enabled:
            register_interval_job(self.internal_name(),
                title=self.fullname(), func=self.execute,
                kwargs={'source_id': self.pk}, seconds=self.interval
            )

    def execute(self, source_id):
        source = WatchFolder.objects.get(pk=source_id)
        if source.uncompress == SOURCE_UNCOMPRESS_CHOICE_Y:
            expand = True
        else:
            expand = False
        print 'execute: %s' % self.internal_name()

    class Meta(BaseModel.Meta):
        verbose_name = _(u'watch folder')
        verbose_name_plural = _(u'watch folders')


class OutOfProcess(BaseModel):
    is_interactive = False

    class Meta(BaseModel.Meta):
        verbose_name = _(u'out of process')
        verbose_name_plural = _(u'out of process')
