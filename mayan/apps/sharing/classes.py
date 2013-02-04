from __future__ import absolute_import

import errno
import logging
import os

from .settings import FILESYSTEM_SERVING

logger = logging.getLogger(__name__)


class SharingBase(object):
    pass


class LocalFilesystem(SharingBase):
    @classmethod
    def _assemble_path_from_list(cls, directory_list):
        return os.path.normpath(os.sep.join(directory_list))        

    @classmethod
    def _get_instance_path(cls, node_instance):
        """
        Return a platform formated filesytem path corresponding to an
        index instance
        """
        names = []
        for ancestor in node_instance.get_ancestors():
            names.append(ancestor.value)

        names.append(node_instance.value)
        logger.debug('names: %s' % names)

        return cls._assemble_path_from_list(names)

    def create_node(self, node_instance):
        logger.debug('node_instance: %s' % node_instance)
        logger.debug('ancestors: %s' % node_instance.get_ancestors())
        
        if node_instance.index.name in FILESYSTEM_SERVING:
            logger.debug('FILESYSTEM_SERVING: %s' % FILESYSTEM_SERVING)

            target_directory = LocalFilesystem._assemble_path_from_list([FILESYSTEM_SERVING[node_instance.index.name], LocalFilesystem._get_instance_path(node_instance)])
            logger.debug('target_directory: %s' % target_directory)

            try:
                os.mkdir(target_directory)
            except OSError, exc:
                if exc.errno == errno.EEXIST:
                    # Nevermid if the directory already exists
                    pass
                else:
                    raise Exception('Unable to create indexing directory; %s' % exc)    

    def delete_node(self, node_instance):
        if node_instance.index_template_node.index.name in FILESYSTEM_SERVING:
            target_directory = LocalFilesystem._assemble_path_from_list([FILESYSTEM_SERVING[node_instance.index_template_node.index.name], LocalFilesystem._get_instance_path(node_instance)])
            try:
                os.removedirs(target_directory)
            except OSError, exc:
                if exc.errno == errno.ENOENT or exc.errno == errno.ENOTEMPTY:
                    pass
                else:
                    raise Exception('Unable to delete indexing directory; %s' % exc)
