from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from documents.permissions import (PERMISSION_DOCUMENT_NEW_VERSION, 
    PERMISSION_DOCUMENT_CREATE)
from navigation.classes import Link

from .icons import (icon_staging_file_delete,
    icon_setup_sources, icon_setup_web_form_list, icon_setup_staging_folder_list,
    icon_setup_watch_folder_list, icon_setup_source_edit,
    icon_setup_source_delete, icon_setup_source_create,
    icon_setup_source_log_list, icon_source_list, icon_upload_version,
    icon_document_create_multiple, icon_create_siblings)

from .models import (WebForm, StagingFolder, SourceTransformation,
    WatchFolder)
from .permissions import (PERMISSION_SOURCES_SETUP_VIEW,
    PERMISSION_SOURCES_SETUP_EDIT, PERMISSION_SOURCES_SETUP_DELETE,
    PERMISSION_SOURCES_SETUP_CREATE)

setup_source_transformation_list = Link(text=_(u'transformations'), view='setup_source_transformation_list', args=['source.source_type', 'source.pk'], permissions=[PERMISSION_SOURCES_SETUP_EDIT]) # TODO: icon 'famfam': 'shape_move_front',
setup_source_transformation_create = Link(text=_(u'add transformation'), view='setup_source_transformation_create', args=['source.source_type', 'source.pk'], permissions=[PERMISSION_SOURCES_SETUP_EDIT]) # TODO icon: 'famfam': 'shape_square_add'
setup_source_transformation_edit = Link(text=_(u'edit'), view='setup_source_transformation_edit', args='transformation.pk', permissions=[PERMISSION_SOURCES_SETUP_EDIT])# 'famfam': 'shape_square_edit', 
setup_source_transformation_delete = Link(text=_(u'delete'), view='setup_source_transformation_delete', args='transformation.pk', permissions=[PERMISSION_SOURCES_SETUP_EDIT]) #'famfam': 'shape_square_delete', 

staging_file_delete = Link(text=_(u'delete'), view='staging_file_delete', args=['source.source_type', 'source.pk', 'object.pk'], icon=icon_staging_file_delete, keep_query=True, permissions=[PERMISSION_DOCUMENT_NEW_VERSION, PERMISSION_DOCUMENT_CREATE])

setup_sources = Link(text=_(u'sources'), view='setup_web_form_list', icon=icon_setup_sources, permissions=[PERMISSION_SOURCES_SETUP_VIEW])
setup_web_form_list = Link(text=_(u'web forms'), view='setup_web_form_list', icon=icon_setup_web_form_list, permissions=[PERMISSION_SOURCES_SETUP_VIEW])
setup_staging_folder_list = Link(text=_(u'staging folders'), view='setup_staging_folder_list', icon=icon_setup_staging_folder_list, permissions=[PERMISSION_SOURCES_SETUP_VIEW])
setup_watch_folder_list = Link(text=_(u'watch folders'), view='setup_watch_folder_list', icon=icon_setup_watch_folder_list, permissions=[PERMISSION_SOURCES_SETUP_VIEW])

setup_source_edit = Link(text=_(u'edit'), view='setup_source_edit', args=['source.source_type', 'source.pk'], icon=icon_setup_source_edit, permissions=[PERMISSION_SOURCES_SETUP_EDIT])
setup_source_delete = Link(text=_(u'delete'), view='setup_source_delete', args=['source.source_type', 'source.pk'], icon=icon_setup_source_delete, permissions=[PERMISSION_SOURCES_SETUP_DELETE])
setup_source_create = Link(text=_(u'add new source'), view='setup_source_create', args='source_type', icon=icon_setup_source_create, permissions=[PERMISSION_SOURCES_SETUP_CREATE])

source_list = Link(text=_(u'Document sources'), view='setup_web_form_list', icon=icon_source_list, children_url_regex=[r'sources/setup'], permissions=[PERMISSION_SOURCES_SETUP_VIEW])

upload_version = Link(text=_(u'upload new version'), view='upload_version', args='object.pk', icon=icon_upload_version, permissions=[PERMISSION_DOCUMENT_NEW_VERSION])

document_create_multiple = Link(text=_(u'upload new documents'), view='document_create_multiple', permissions=[PERMISSION_DOCUMENT_CREATE], children_view_regex=[r'upload_interactive'], icon=icon_document_create_multiple)
document_create_siblings = Link(text=_(u'clone metadata'), view='document_create_siblings', args='object.id', icon=icon_create_siblings, permissions=[PERMISSION_DOCUMENT_CREATE])
