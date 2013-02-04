"""Configuration options for the document_indexing app"""

from django.utils.translation import ugettext_lazy as _

from smart_settings.api import register_settings

register_settings(
    namespace=u'sharing',
    module=u'sharing.settings',
    settings=[
        # Definition
        {'name': u'SUFFIX_SEPARATOR', 'global_name': u'SHARING_SUFFIX_SEPARATOR', 'default': u'_'},
        # Filesystem serving
        {'name': u'SLUGIFY_PATHS', 'global_name': u'SHARING_SLUGIFY_PATHS', 'default': False},
        {'name': u'MAX_SUFFIX_COUNT', 'global_name': u'SHARING_MAX_SUFFIX_COUNT', 'default': 1000},
        {'name': u'FILESYSTEM_SERVING', 'global_name': u'SHARING_FILESYSTEM_SERVING', 'default': {}, 'description': _(u'A dictionary that maps the index name and where on the filesystem that index will be mirrored.')}
    ]
)
