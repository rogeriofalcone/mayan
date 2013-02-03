from django.dispatch import Signal

create_node_instance = Signal(providing_args=['index_instance'])
add_document_to_node_instance = Signal(providing_args=['index_instance', 'document'])
remove_document_from_node_instance = Signal(providing_args=['index_instance', 'document'])
delete_node_instance = Signal(providing_args=['index_instance'])
