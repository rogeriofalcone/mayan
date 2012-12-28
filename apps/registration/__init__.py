from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.db import transaction, DatabaseError
from navigation.api import register_links
from common.links import about_view, license_view

from .models import RegistrationSingleton
from .links import form_view

register_links(['form_view'], [about_view, license_view], menu_name='secondary_menu')
register_links(['form_view', 'about_view', 'license_view'], [form_view], menu_name='secondary_menu')

with transaction.commit_on_success():
    try:
        RegistrationSingleton.objects.get()
    except DatabaseError:
        transaction.rollback()
