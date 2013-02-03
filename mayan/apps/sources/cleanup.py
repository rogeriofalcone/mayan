from __future__ import absolute_import


def cleanup():
    from .models import StagingFolder, WebForm

    StagingFolder.objects.all().delete()
    WebForm.objects.all().delete()
