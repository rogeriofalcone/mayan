# -*- coding: utf-8 -*-
from __future__ import absolute_import

import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

from documents.models import DocumentPageTransformation, DocumentPage
from sources.models import SourceTransformation
from ocr.models import QueueTransformation

from ..models import Transformation


class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."
        
        # Get document pages' tranformations
        for document_page_transformation in DocumentPageTransformation.objects.all():
            try:
                transformation = Transformation.objects.create(
                    content_object=document_page_transformation.document_page,
                    transformation=document_page_transformation.transformation,
                    arguments=document_page_transformation.arguments,
                    order=document_page_transformation.order,
                )
            except DocumentPage.DoesNotExist:
                pass

        # Get sources' tranformations
        for source_transformation in SourceTransformation.objects.all():
            transformation = Transformation.objects.create(
                content_object=source_transformation.content_object,
                transformation=source_transformation.transformation,
                arguments=source_transformation.arguments,
                order=source_transformation.order,
            )

        # Get queues' tranformations
        for queue_transformation in QueueTransformation.objects.all():
            transformation = Transformation.objects.create(
                content_object=queue_transformation.content_object,
                transformation=queue_transformation.transformation,
                arguments=queue_transformation.arguments,
                order=queue_transformation.order,
            )

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'converter.transformation': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Transformation'},
            'arguments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_pk': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'transformation': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['converter']
    symmetrical = True
