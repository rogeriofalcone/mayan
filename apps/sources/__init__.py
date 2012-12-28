from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import (register_links,
    register_model_list_columns)
from common.utils import encapsulate
from project_setup.api import register_setup
from documents.permissions import (PERMISSION_DOCUMENT_NEW_VERSION, 
    PERMISSION_DOCUMENT_CREATE)

from .staging import StagingFile
from .models import (WebForm, StagingFolder, SourceTransformation,
    WatchFolder)
from .widgets import staging_file_thumbnail
from .links import (staging_file_preview, staging_file_delete, setup_sources,
    setup_web_form_list, setup_staging_folder_list, setup_watch_folder_list,
    setup_source_edit, setup_source_delete, setup_source_create,
    setup_source_transformation_list, setup_source_transformation_create,
    setup_source_transformation_edit, setup_source_transformation_delete,
    source_list, upload_version)


register_links(StagingFile, [staging_file_delete])

register_links(SourceTransformation, [setup_source_transformation_edit, setup_source_transformation_delete])

#register_links(['setup_web_form_list', 'setup_staging_folder_list', 'setup_watch_folder_list', 'setup_source_create'], [setup_web_form_list, setup_staging_folder_list, setup_watch_folder_list], menu_name='form_header')
register_links(['setup_web_form_list', 'setup_staging_folder_list', 'setup_watch_folder_list', 'setup_source_create'], [setup_web_form_list, setup_staging_folder_list], menu_name='form_header')

#register_links(WebForm, [setup_web_form_list, setup_staging_folder_list, setup_watch_folder_list], menu_name='form_header')
register_links(WebForm, [setup_web_form_list, setup_staging_folder_list], menu_name='form_header')
register_links(WebForm, [setup_source_transformation_list, setup_source_edit, setup_source_delete])

register_links(['setup_web_form_list', 'setup_staging_folder_list', 'setup_watch_folder_list', 'setup_source_edit', 'setup_source_delete', 'setup_source_create'], [setup_sources, setup_source_create], menu_name='sidebar')

#register_links(StagingFolder, [setup_web_form_list, setup_staging_folder_list, setup_watch_folder_list], menu_name='form_header')
register_links(StagingFolder, [setup_web_form_list, setup_staging_folder_list], menu_name='form_header')
register_links(StagingFolder, [setup_source_transformation_list, setup_source_edit, setup_source_delete])

register_links(WatchFolder, [setup_web_form_list, setup_staging_folder_list, setup_watch_folder_list], menu_name='form_header')
register_links(WatchFolder, [setup_source_transformation_list, setup_source_edit, setup_source_delete])

# Document version
register_links(['document_version_list', 'upload_version', 'document_version_revert'], [upload_version], menu_name='sidebar')

register_links(['setup_source_transformation_create', 'setup_source_transformation_edit', 'setup_source_transformation_delete', 'setup_source_transformation_list'], [setup_source_transformation_create], menu_name='sidebar')

source_views = ['setup_web_form_list', 'setup_staging_folder_list', 'setup_watch_folder_list', 'setup_source_edit', 'setup_source_delete', 'setup_source_create', 'setup_source_transformation_list', 'setup_source_transformation_edit', 'setup_source_transformation_delete', 'setup_source_transformation_create']

register_model_list_columns(StagingFile, [
        {'name':_(u'thumbnail'), 'attribute':
            encapsulate(lambda x: staging_file_thumbnail(x))
        },
    ])

register_setup(setup_sources)
