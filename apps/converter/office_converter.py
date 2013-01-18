from __future__ import absolute_import

import os
import logging

import sh

from mimetype.api import get_mimetype
from common.conf.settings import TEMPORARY_DIRECTORY

from .conf.settings import LIBREOFFICE_PATH
from .exceptions import (OfficeConversionError,
    OfficeBackendError, UnknownFileFormat)

CACHED_FILE_SUFFIX = u'_office_converter'

CONVERTER_OFFICE_FILE_MIMETYPES = [
    u'application/msword',
    u'application/mswrite',
    u'application/mspowerpoint',
    u'application/msexcel',
    u'application/vnd.ms-excel',
    u'application/vnd.ms-powerpoint',
    u'application/vnd.oasis.opendocument.presentation',
    u'application/vnd.oasis.opendocument.text',
    u'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    u'application/vnd.oasis.opendocument.spreadsheet',
    u'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    u'application/vnd.oasis.opendocument.graphics',
    u'application/vnd.ms-office',
    u'text/plain',
    u'text/rtf',
]

logger = logging.getLogger(__name__)


class OfficeConverter(object):
    def __init__(self):
        self.backend_class = OfficeConverterBackendDirect
        self.backend = self.backend_class()
        self.exists = False
        self.mimetype = None
        self.encoding = None

    def mimetypes(self):
        return CONVERTER_OFFICE_FILE_MIMETYPES

    def convert(self, input_filepath, mimetype=None):
        self.exists = False
        self.mimetype = None
        self.encoding = None

        self.input_filepath = input_filepath

        # Make sure file is of a known office format
        if mimetype:
            self.mimetype = mimetype
        else:
            self.mimetype, self.encoding = get_mimetype(open(self.input_filepath), self.input_filepath, mimetype_only=True)

        if self.mimetype in CONVERTER_OFFICE_FILE_MIMETYPES:
            # Cache results of conversion
            self.output_filepath = os.path.join(TEMPORARY_DIRECTORY, u''.join([self.input_filepath, CACHED_FILE_SUFFIX]))
            self.exists = os.path.exists(self.output_filepath)
            if not self.exists:
                try:
                    self.backend.convert(self.input_filepath, self.output_filepath)
                    self.exists = True
                except OfficeBackendError, msg:
                    # convert exception so that at least the mime type icon is displayed
                    raise UnknownFileFormat(msg)

    def __unicode__(self):
        return getattr(self, 'output_filepath', None)

    def __str__(self):
        return str(self.__unicode__())


class OfficeConverterBackendDirect(object):
    def __init__(self):
        self.binary = sh.Command(LIBREOFFICE_PATH)
        try:
            self.version_info = self.binary('-V').stdout
        except sh.CommandNotFound:
            raise OfficeBackendError('Error initializing LibreOffice backend, cannot find LibreOffice executable.')
        except Exception as exception:
            raise OfficeBackendError('Error initializing LibreOffice backend; %s' % exception.stderr)

    def convert(self, input_filepath, output_filepath):
        """
        Executes libreoffice using the sh library
        """
        new_environment = os.environ.copy()
        new_environment['HOME'] = TEMPORARY_DIRECTORY

        try:
            self.binary('--headless', '--convert-to', 'pdf', input_filepath, '--outdir', TEMPORARY_DIRECTORY, _env=new_environment)
        except Exception as exception:
            raise OfficeBackendError('LibreOffice PDF conversion error; %s' % (exception.stderr or 'No error message return by LibreOffice'))
        else:
            try:
                filename, extension = os.path.splitext(os.path.basename(input_filepath))
                logger.debug('filename: %s' % filename)
                logger.debug('extension: %s' % extension)

                converted_output = os.path.join(TEMPORARY_DIRECTORY, os.path.extsep.join([filename, 'pdf']))
                logger.debug('converted_output: %s' % converted_output)
             
                os.rename(converted_output, output_filepath)      
            except OSError as exception:
                raise OfficeBackendError('Office document conversion failed; %s' % exception)
            except Exception as exception:
                logger.error('Unhandled exception; %s' % exception)
