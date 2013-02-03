from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from common.utils import encapsulate
from converter.links import link_transformation_list
from documents.models import Document
from navigation.api import register_model_list_columns
from navigation.classes import Link
from project_setup.api import register_setup

from .links import (staging_file_delete, setup_sources,
    setup_web_form_list, setup_staging_folder_list, setup_watch_folder_list,
    setup_source_edit, setup_source_delete, setup_web_form_create, setup_staging_folder_create,
    upload_version, document_create_multiple, document_create_siblings)
from .models import WebForm, StagingFolder, WatchFolder, InteractiveBaseModel
from .staging import StagingFile
from .widgets import staging_file_thumbnail

Link.bind_links([StagingFile], [staging_file_delete])

Link.bind_links(['setup_web_form_list', 'setup_staging_folder_list', 'setup_watch_folder_list', 'setup_source_create', 'setup_source_create_staging_folder', 'setup_source_create_web_form'], [setup_web_form_list, setup_staging_folder_list], menu_name='form_header')

Link.bind_links([InteractiveBaseModel], [setup_web_form_list, setup_staging_folder_list], menu_name='form_header')
Link.bind_links([InteractiveBaseModel], [link_transformation_list, setup_source_edit, setup_source_delete])

Link.bind_links([WebForm, 'setup_web_form_list', 'setup_source_create_web_form'], [setup_web_form_create], menu_name='secondary_menu')
Link.bind_links([StagingFolder, 'setup_staging_folder_list', 'setup_source_create_staging_folder'], [setup_staging_folder_create], menu_name='secondary_menu')

# Document version
Link.bind_links(['document_version_list', 'upload_version', 'document_version_revert'], [upload_version], menu_name='sidebar')

Link.bind_links(['document_list_recent', 'document_list', 'document_create', 'upload_interactive', 'staging_file_delete', 'document_create_multiple'], [document_create_multiple], menu_name='secondary_menu')

Link.bind_links([Document], document_create_multiple, menu_name='secondary_menu')
Link.bind_links([Document], document_create_siblings)

register_model_list_columns(StagingFile, [
        {'name':_(u'thumbnail'), 'attribute':
            encapsulate(lambda x: staging_file_thumbnail(x))
        },
    ])

register_setup(setup_sources)
