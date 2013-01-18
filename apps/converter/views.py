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
from permissions.models import Permission

from .api import get_format_list
from .classes import TransformationSourceObject
from .conf.settings import GRAPHICS_BACKEND
from .forms import TransformationForm_create, TransformationForm
from .models import Transformation
from .permissions import (PERMISSION_TRANSFORMATION_CREATE, PERMISSION_TRANSFORMATION_DELETE,
    PERMISSION_TRANSFORMATION_EDIT, PERMISSION_TRANSFORMATION_VIEW)


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
    obj = get_object_or_404(content_type.model_class(), pk=object_pk)
    
    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_TRANSFORMATION_VIEW])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_TRANSFORMATION_VIEW, request.user, obj)

    context = {
        'object_list': Transformation.objects.for_model(obj),
        'title': _(u'transformatioeens for: %s' % obj),
        'extra_columns': [
            {'name': _(u'order'), 'attribute': 'order'},
            {'name': _(u'transformation'), 'attribute': encapsulate(lambda x: x.get_transformation_display())},
            {'name': _(u'arguments'), 'attribute': 'arguments'}
        ],
        'hide_object': True,
        'object': obj,
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def transformation_create(request, app_label, module_name, object_pk):
    content_type = get_object_or_404(ContentType, app_label=app_label, model=module_name)
    obj = get_object_or_404(content_type.model_class(), pk=object_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_TRANSFORMATION_CREATE])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_TRANSFORMATION_CREATE, request.user, obj)

    redirect_view = '/' # FIX reverse('setup_source_transformation_list', args=[source.source_type, source.pk])

    if request.method == 'POST':
        form = TransformationForm_create(request.POST)
        if form.is_valid():
            try:
                source_tranformation = form.save(commit=False)
                source_tranformation.content_object = obj
                source_tranformation.save()
                messages.success(request, _(u'Transformation created successfully'))
                return HttpResponseRedirect(redirect_view)
            except Exception, e:
                messages.error(request, _(u'Error creating transformation; %s') % e)
    else:
        form = TransformationForm_create()

    context = {
        'form': form,
        'title': _(u'add transformation for: %s') % obj,
        'object': obj,
    }

    return render_to_response('generic_form.html', context,
        context_instance=RequestContext(request))


def transformation_edit(request, transformation_pk):
    Permission.objects.check_permissions(request.user, [PERMISSION_TRANSFORMATION_EDIT])

    source_transformation = get_object_or_404(Transformation, pk=transformation_pk)
    redirect_view = '/' # FIX reverse('setup_source_transformation_list', args=[source_transformation.content_object.source_type, source_transformation.content_object.pk])
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', redirect_view)))

    if request.method == 'POST':
        form = TransformationForm(instance=source_transformation, data=request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _(u'Transformation edited successfully'))
                return HttpResponseRedirect(next)
            except Exception, e:
                messages.error(request, _(u'Error editing transformation; %s') % e)
    else:
        form = TransformationForm(instance=source_transformation)

    return render_to_response('generic_form.html', {
        'title': _(u'Edit transformation: %s') % source_transformation,
        'form': form,
        'source_object': source_transformation.content_object,
        'object': source_transformation,
        'navigation_object_list': [
            {'object': 'source_object'},
            {'object': 'object'},
        ],        
        'next': next,
    },
    context_instance=RequestContext(request))


def transformation_delete(request, transformation_pk):
    Permission.objects.check_permissions(request.user, [PERMISSION_TRANSFORMATION_DELETE])

    source_transformation = get_object_or_404(Transformation, pk=transformation_pk)
    redirect_view = '/'# FIX reverse('setup_source_transformation_list', args=[source_transformation.content_object.source_type, source_transformation.content_object.pk])
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', redirect_view)))

    if request.method == 'POST':
        try:
            source_transformation.delete()
            messages.success(request, _(u'Transformation deleted successfully.'))
        except Exception, e:
            messages.error(request, _(u'Error deleting transformation; %(error)s') % {
                'error': e}
            )
        return HttpResponseRedirect(redirect_view)

    return render_to_response('generic_confirm.html', {
        'delete_view': True,
        'source_object': source_transformation.content_object,
        'object': source_transformation,
        'navigation_object_list': [
            {'object': 'source_object'},
            {'object': 'object'},
        ],
        'title': _(u'Are you sure you wish to delete source transformation "%(transformation)s"') % {
            'transformation': source_transformation.get_transformation_display(),
        },
        'previous': previous,
        'form_icon': u'shape_square_delete.png',
    },
    context_instance=RequestContext(request))
