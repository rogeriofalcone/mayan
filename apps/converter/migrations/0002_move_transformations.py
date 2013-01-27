# -*- coding: utf-8 -*-
from __future__ import absolute_import

import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.contrib.contenttypes.models import ContentType

from ..models import Transformation


class Migration(DataMigration):
    depends_on = (
        ('documents', '0015_auto__add_unique_documenttype_name'),
        ('sources', '0001_initial'),
        ('ocr', '0001_initial'),
    )

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."
        # Get document pages' tranformations
        for document_page_transformation in orm['documents.documentpagetransformation'].objects.all():
            try:
                transformation = Transformation.objects.create(
                    content_object=document_page_transformation.document_page,
                    transformation=document_page_transformation.transformation,
                    arguments=document_page_transformation.arguments,
                    order=document_page_transformation.order,
                )
            except orm['documents.documentpage'].DoesNotExist:
                pass

        # Get sources' tranformations
        for source_transformation in orm['sources.sourcetransformation'].objects.all():
            transformation = Transformation.objects.create(
                # User proper call to ContentType until 
                # the contenttype instance returned is fixed in South
                # https://groups.google.com/forum/?fromgroups=#!topic/south-users/h85BGCdCb8A%5B1-25-false%5D
                #content_type=source_transformation.content_type,
                #content_type=ContentType.objects.get(app_label="sources", model="sourcetransformation"),
                #object_pk=source_transformation.object_id,
                content_object=source_transformation.content_object,
                transformation=source_transformation.transformation,
                arguments=source_transformation.arguments,
                order=source_transformation.order,
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
        },
        'documents.documenttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'DocumentType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        },
        'documents.document': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Document'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'document_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documents.DocumentType']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '48', 'blank': 'True'})
        },
        'documents.documentversion': {
            'Meta': {'unique_together': "(('document', 'major', 'minor', 'micro', 'release_level', 'serial'),)", 'object_name': 'DocumentVersion'},
            'checksum': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documents.Document']"}),
            'encoding': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'filename': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'major': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'micro': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'mimetype': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'minor': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'release_level': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'serial': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        'documents.documentpage': {
            'Meta': {'ordering': "['page_number']", 'object_name': 'DocumentPage'},
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'document_version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documents.DocumentVersion']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page_label': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'page_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'db_index': 'True'})
        },
        'documents.documentpagetransformation': {
            'Meta': {'ordering': "('order',)", 'object_name': 'DocumentPageTransformation'},
            'arguments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'document_page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documents.DocumentPage']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'transformation': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'sources.sourcetransformation': {
            'Meta': {'ordering': "('order',)", 'object_name': 'SourceTransformation'},
            'arguments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'transformation': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
       'ocr.queuetransformation': {
            'Meta': {'ordering': "('order',)", 'object_name': 'QueueTransformation'},
            'arguments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'transformation': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
    }

    complete_apps = ['converter']
    symmetrical = True
