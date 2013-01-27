from __future__ import absolute_import


def delete_transformations():
    from .models import Transformation

    Transformation.objects.all().delete()
