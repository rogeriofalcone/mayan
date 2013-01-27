from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.classes import Link

from .icons import icon_registration
from .models import RegistrationSingleton


def is_not_registered(context):
    return RegistrationSingleton.registration_state() == False
    

link_registration_form = Link(text=_(u'Registration'), view='form_view', condition=is_not_registered, icon=icon_registration)
