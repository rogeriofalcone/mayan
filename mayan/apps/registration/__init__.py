from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.db import transaction, DatabaseError

from common.links import link_about, link_license
from navigation.classes import Link

from .links import link_registration_form
from .models import RegistrationSingleton

Link.bind_links(['form_view'], [link_about, link_license], menu_name='secondary_menu')
Link.bind_links(['form_view', 'about_view', 'license_view'], [link_registration_form], menu_name='secondary_menu')

with transaction.commit_on_success():
    try:
        RegistrationSingleton.objects.get()
    except DatabaseError:
        transaction.rollback()
