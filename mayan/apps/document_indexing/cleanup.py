from __future__ import absolute_import

from .models import Index


def cleanup():
    Index.objects.all().delete()
