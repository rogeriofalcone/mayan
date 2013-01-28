from __future__ import absolute_import

from django.core.exceptions import PermissionDenied
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.translation import ugettext_lazy as _

from .classes import Statistic, StatisticNamespace


def statistics_list(request):
    if not request.user.is_superuser or not request.user.is_staff:
        raise PermissionDenied

    return render_to_response('generic_list.html', {
        'object_list': StatisticNamespace.get_all(),
        'title': _(u'statistics namespaces')
    },
    context_instance=RequestContext(request))


def namespace_details(request, namespace_id):
    if not request.user.is_superuser or not request.user.is_staff:
        raise PermissionDenied
    
    namespace = StatisticNamespace.get(namespace_id)

    return render_to_response('generic_list.html', {
        'object': namespace,
        'object_list': namespace.statistics,
        'title': _(u'namespace details for: %s') % namespace,
    },
    context_instance=RequestContext(request))
    
def execute(request, statistic_id):
    if not request.user.is_superuser or not request.user.is_staff:
        raise PermissionDenied
    
    statictic = Statistic.get(statistic_id)

    return render_to_response('generic_list.html', {
        'object': statictic, 
        'object_list': statictic.get_results(),
        'title': _(u'results for: %s') % statictic,
    },
    context_instance=RequestContext(request))
