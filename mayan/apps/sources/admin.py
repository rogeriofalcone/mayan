from __future__ import absolute_import

from django.contrib import admin

from .models import StagingFolder, WebForm

admin.site.register(StagingFolder)
admin.site.register(WebForm)
