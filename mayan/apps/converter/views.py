from __future__ import absolute_import

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from acls.models import AccessEntry
from common.utils import encapsulate
from documents.models import Document
from permissions.models import Permission

from .api import get_format_list
from .classes import MenuLessObject
from .forms import TransformationForm_create, TransformationForm
from .icons import icon_transformation_clear
from .models import Transformation
from .permissions import (PERMISSION_TRANSFORMATION_CREATE, PERMISSION_TRANSFORMATION_DELETE,
    PERMISSION_TRANSFORMATION_EDIT, PERMISSION_TRANSFORMATION_VIEW, PERMISSION_DOCUMENT_TRANSFORM)
from .settings import GRAPHICS_BACKEND


def formats_list(request):
    if request.user.is_superuser or request.user.is_staff:
        context = {
            'title': _(u'suported file formats'),
            'hide_object': True,
            'object_list': sorted(get_format_list()),
            'extra_columns': [
                {
                    'name': _(u'name'),
                    'attribute': encapsulate(lambda x: x[0])
                },
                {
                    'name': _(u'description'),
                    'attribute': encapsulate(lambda x: x[1])
                }
            ],
            'backend': GRAPHICS_BACKEND,
        }

        return render_to_response('generic_list.html', context,
            context_instance=RequestContext(request))
    else:
        raise PermissionDenied


def transformation_list(request, app_label, module_name, object_pk):
    content_type = get_object_or_404(ContentType, app_label=app_label, model=module_name)
    content_object = get_object_or_404(content_type.model_class(), pk=object_pk)
    
    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_TRANSFORMATION_VIEW])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_TRANSFORMATION_VIEW, request.user, content_object)

    context = {
        'object_list': Transformation.objects.for_model(content_object),
        'title': _(u'transformation for %(object_label)s: %(object)s') % {
            'object_label': content_object._meta.verbose_name,
            'object': content_object
        },
        'extra_columns': [
            {'name': _(u'order'), 'attribute': 'order'},
            {'name': _(u'transformation'), 'attribute': encapsulate(lambda x: x.get_transformation_display())},
            {'name': _(u'arguments'), 'attribute': 'arguments'}
        ],
        'hide_object': True,
        'source_object': content_object,
        'navigation_object_list': [
            {'object': 'source_object'},
        ],            
    }
    
    if isinstance(content_object, MenuLessObject.get_all_objects()):
        context['web_theme_hide_menus'] = True

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def transformation_create(request, app_label, module_name, object_pk):
    content_type = get_object_or_404(ContentType, app_label=app_label, model=module_name)
    content_object = get_object_or_404(content_type.model_class(), pk=object_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_TRANSFORMATION_CREATE])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_TRANSFORMATION_CREATE, request.user, content_object)

    redirect_view = reverse('transformation_list', args=[content_object._meta.app_label, content_object._meta.module_name, content_object.pk])
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse('home'))))

    if request.method == 'POST':
        form = TransformationForm_create(request.POST)
        if form.is_valid():
            try:
                source_tranformation = form.save(commit=False)
                source_tranformation.content_object = content_object
                source_tranformation.save()
                messages.success(request, _(u'Transformation created successfully'))
                return HttpResponseRedirect(redirect_view)
            except Exception, e:
                messages.error(request, _(u'Error creating transformation; %s') % e)
    else:
        form = TransformationForm_create()

    context = {
        'form': form,
        'title': _(u'add transformation for %(object_label)s: %(object)s') % {
            'object_label': content_object._meta.verbose_name,
            'object': content_object
        },
        'source_object': content_object,
        'navigation_object_list': [
            {'object': 'source_object'},
        ],  
        'previous': previous,
    }
    
    if isinstance(content_object, MenuLessObject.get_all_objects()):
        context['web_theme_hide_menus'] = True

    return render_to_response('generic_form.html', context,
        context_instance=RequestContext(request))


def transformation_edit(request, transformation_pk):
    transformation = get_object_or_404(Transformation, pk=transformation_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_TRANSFORMATION_EDIT])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_TRANSFORMATION_EDIT, request.user, transformation.content_object)

    redirect_view = reverse('transformation_list', args=[transformation.content_object._meta.app_label, transformation.content_object._meta.module_name, transformation.content_object.pk])
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', redirect_view)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse('home'))))

    if request.method == 'POST':
        form = TransformationForm(instance=transformation, data=request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _(u'Transformation edited successfully'))
                return HttpResponseRedirect(next)
            except Exception, e:
                messages.error(request, _(u'Error editing transformation; %s') % e)
    else:
        form = TransformationForm(instance=transformation)

    context = {
        'title': _(u'Edit transformation: %s') % transformation,
        'form': form,
        'source_object': transformation.content_object,
        'object': transformation,
        'navigation_object_list': [
            {'object': 'source_object'},
            {'object': 'object'},
        ],        
        'next': next,
        'previous': previous,
    }

    if isinstance(transformation.content_object, MenuLessObject.get_all_objects()):
        context['web_theme_hide_menus'] = True

    return render_to_response('generic_form.html', context,
        context_instance=RequestContext(request))


def transformation_delete(request, transformation_pk):
    transformation = get_object_or_404(Transformation, pk=transformation_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_TRANSFORMATION_DELETE])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_TRANSFORMATION_DELETE, request.user, transformation.content_object)

    redirect_view = reverse('transformation_list', args=[transformation.content_object._meta.app_label, transformation.content_object._meta.module_name, transformation.content_object.pk])
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse('home'))))

    if request.method == 'POST':
        try:
            transformation.delete()
            messages.success(request, _(u'Transformation deleted successfully.'))
        except Exception, e:
            messages.error(request, _(u'Error deleting transformation; %(error)s') % {
                'error': e}
            )
        return HttpResponseRedirect(redirect_view)

    context = {
            'delete_view': True,
            'source_object': transformation.content_object,
            'object': transformation,
            'navigation_object_list': [
                {'object': 'source_object'},
                {'object': 'object'},
            ],        
            'title': _(u'Are you sure you wish to delete source transformation "%(transformation)s"') % {
                'transformation': transformation.get_transformation_display(),
            },
        'previous': previous,
        'form_icon': u'shape_square_delete.png',
    }

    if isinstance(transformation.content_object, MenuLessObject.get_all_objects()):
        context['web_theme_hide_menus'] = True

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def document_clear_transformations(request, document_pk=None, document_pk_list=None):
    if document_pk:
        documents = [get_object_or_404(Document.objects, pk=document_pk)]
        post_redirect = reverse('document_view_simple', args=[documents[0].pk])
    elif document_pk_list:
        documents = [get_object_or_404(Document, pk=document_pk) for document_pk in document_pk_list.split(',')]
        post_redirect = None
    else:
        messages.error(request, _(u'Must provide at least one document.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', u'/'))

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_TRANSFORM])
    except PermissionDenied:
        documents = AccessEntry.objects.filter_objects_by_access(PERMISSION_DOCUMENT_TRANSFORM, request.user, documents, exception_on_empty=True)

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', post_redirect or reverse('document_list'))))
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', post_redirect or reverse('document_list'))))

    if request.method == 'POST':
        for document in documents:
            try:
                for document_page in document.pages.all():
                    document_page.document.invalidate_cached_image(document_page.page_number)
                    for transformation in Transformation.objects.for_model(document_page):
                        transformation.delete()
                messages.success(request, _(u'All the page transformations for document: %s, have been deleted successfully.') % document)
            except Exception, e:
                messages.error(request, _(u'Error deleting the page transformations for document: %(document)s; %(error)s.') % {
                    'document': document, 'error': e})

        return HttpResponseRedirect(next)

    context = {
        'object_name': _(u'document transformation'),
        'delete_view': True,
        'previous': previous,
        'next': next,
        'form_icon': icon_transformation_clear,
    }

    if len(documents) == 1:
        context['object'] = documents[0]
        context['title'] = _(u'Are you sure you wish to clear all the page transformations for document: %s?') % ', '.join([unicode(d) for d in documents])
    elif len(documents) > 1:
        context['title'] = _(u'Are you sure you wish to clear all the page transformations for documents: %s?') % ', '.join([unicode(d) for d in documents])

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def document_multiple_clear_transformations(request):
    return document_clear_transformations(request, document_pk_list=request.GET.get('id_list', []))
