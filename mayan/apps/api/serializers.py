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
