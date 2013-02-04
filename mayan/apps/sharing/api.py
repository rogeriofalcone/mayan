from django.template.defaultfilters import slugify

from .exceptions import MaxSuffixCountReached
from .settings import (AVAILABLE_INDEXING_FUNCTIONS,
    MAX_SUFFIX_COUNT, SLUGIFY_PATHS)

if SLUGIFY_PATHS == False:
    # Do not slugify path or filenames and extensions
    SLUGIFY_FUNCTION = lambda x: x
else:
    SLUGIFY_FUNCTION = slugify

# Internal functions
def find_lowest_available_suffix(index_instance, document):
    index_instance_documents = DocumentRenameCount.objects.filter(index_instance_node=index_instance)
    files_list = []
    for index_instance_document in index_instance_documents:
        files_list.append(assemble_suffixed_filename(index_instance_document.document.file_filename, index_instance_document.suffix))

    for suffix in xrange(MAX_SUFFIX_COUNT):
        if assemble_suffixed_filename(document.file_filename, suffix) not in files_list:
            return suffix

    raise MaxSuffixCountReached(ugettext(u'Maximum suffix (%s) count reached.') % MAX_SUFFIX_COUNT)

#    except DocumentRenameCount.DoesNotExist:
#        return warnings
