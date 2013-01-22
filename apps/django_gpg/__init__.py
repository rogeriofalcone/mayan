from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.classes import Link
from hkp import Key as KeyServerKey
from project_setup.api import register_setup

from .api import Key
from .links import (private_keys, public_keys, key_delete, key_query,
    key_receive, key_setup)

#register_links(['key_delete', 'key_private_list', 'key_public_list', 'key_query'], [private_keys, public_keys, key_query], menu_name='sidebar')
Link.bind_links(['key_delete', 'key_public_list', 'key_query'], [public_keys, key_query], menu_name='sidebar')

Link.bind_links([Key], [key_delete])
Link.bind_links([KeyServerKey], [key_receive])

register_setup(key_setup)
