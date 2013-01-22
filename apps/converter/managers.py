from ast import literal_eval

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode


class TransformationManager(models.Manager):
    def for_model(self, model):
        """
        QuerySet for all transformations for a particular model (either an instance or
        a class).
        """
        ct = ContentType.objects.get_for_model(model)
        qs = self.get_query_set().filter(content_type=ct)
        if isinstance(model, models.Model):
            qs = qs.filter(object_pk=force_unicode(model._get_pk_val()))
        return qs

    def get_for_object_as_list(self, obj):
        warnings = []
        transformations = []
        for transformation in self.for_model(obj).values('transformation', 'arguments'):
            try:
                transformations.append(
                    {
                        'transformation': transformation['transformation'],
                        'arguments': literal_eval(transformation['arguments'].strip())
                    }
                )
            except (ValueError, SyntaxError), e:
                warnings.append(e)

        return transformations, warnings

    def clone(self, source_object, target_object):
        for source_transformation in self.for_model(source_object):
            self.create(
                content_object=target_object,
                order=source_transformation.order,
                transformation=source_transformation.transformation,
                arguments=source_transformation.arguments
            )
