from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group

from rest_framework import serializers

from documents.models import Document, DocumentType


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Document
        fields = ('url', 'document_type', 'uuid', 'date_added', 'description')
        

class DocumentTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DocumentType


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

        
"""
class DocumentResourceSimple(ModelResource):
    model = Document
    fields = ('url', 'pk', 'document_type', 'uuid', 'date_added', 'description', 'tags', 'comments', 'expensive_methods', 'versions')
   
    def versions(self, instance):
        return [
            {
                'version': version.get_formated_version(),
                'major': version.major,
                'minor': version.minor,
                'micro': version.micro,
                'release_level': version.release_level,
                'serial': version.serial,
                'timestamp': version.timestamp,
                'comment': version.comment,
                'mimetype': version.mimetype,
                'encoding': version.encoding,
                'filename': version.filename,
                'checksum': version.checksum,
                'download': reverse('document_version_download', args=[version.pk]),
                'stored_filename': version.file.name,
                # TODO: Add transformations
                'pages': [
                    {
                        'content': page.content,
                        'page_label': page.page_label,
                        'page_number': page.page_number,
                    }
                    for page in version.pages.all()
                ]
                
            }
            for version in instance.versions.all()
        ]

    def expensive_methods(self, instance):
        return []
"""
