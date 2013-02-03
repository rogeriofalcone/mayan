from __future__ import absolute_import

import datetime

from django.db import models

from .settings import RECENT_COUNT


class RecentDocumentManager(models.Manager):
    def add_document_for_user(self, user, document):
        if user.is_authenticated():
            new_recent, created = self.model.objects.get_or_create(user=user, document=document)
            if not created:
                # document already in the recent list, just update the accessed date and time
                new_recent.datetime_accessed = datetime.datetime.now()
                new_recent.save()
            for recent_to_delete in self.model.objects.filter(user=user)[RECENT_COUNT:]:
                recent_to_delete.delete()

    def get_for_user(self, user):
        document_model = models.get_model('documents', 'document')

        if user.is_authenticated():
            return document_model.objects.filter(recentdocument__user=user).order_by('-recentdocument__datetime_accessed')
        else:
            return document_model.objects.none()


class DocumentTypeManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)
