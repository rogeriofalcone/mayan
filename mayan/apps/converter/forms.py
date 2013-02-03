from __future__ import absolute_import

from django import forms
from django.utils.translation import ugettext

from .models import Transformation


class TransformationForm(forms.ModelForm):
    class Meta:
        model = Transformation

    def __init__(self, *args, **kwargs):
        super(TransformationForm, self).__init__(*args, **kwargs)
        self.fields['content_type'].widget = forms.HiddenInput()
        self.fields['object_pk'].widget = forms.HiddenInput()


class TransformationForm_create(forms.ModelForm):
    class Meta:
        model = Transformation
        exclude = ('content_type', 'object_pk')
