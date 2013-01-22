from __future__ import absolute_import

import logging
import re
import urllib
import urlparse

from django.core.urlresolvers import reverse, NoReverseMatch
from django.template import VariableDoesNotExist, Variable
from django.template import (VariableDoesNotExist, Variable)
from django.utils.encoding import smart_str, smart_unicode
from django.utils.http import urlquote, urlencode
from django.utils.translation import ugettext_lazy as _

from .utils import resolve_to_name, resolve_arguments, get_navigation_objects

logger = logging.getLogger(__name__)


class ResolvedLink(object):
    active = False
    url = '#'
    text = _('Unnamed link')


class Link(object):
    bound_links = {}

    @classmethod
    def bind_links(cls, sources, links, menu_name=None, position=0):
        """
        Associate a link to a model, a view, or an url
        """
        cls.bound_links.setdefault(menu_name, {})
        try:
            for source in sources:
                cls.bound_links[menu_name].setdefault(source, {'links': []})
                try:
                    cls.bound_links[menu_name][source]['links'].extend(links)
                except TypeError:
                    # Try to see if links is a single link
                    cls.bound_links[menu_name][source]['links'].append(links)
        except TypeError:
            raise Exception('The bind_links source argument must be a list, even for single element sources.')

    def __init__(self, text, view, klass=None, args=None, icon=None,
        permissions=None, condition=None, conditional_disable=None,
        description=None, dont_mark_active=False, children_view_regex=None,
        keep_query=False, children_classes=None, children_url_regex=None,
        children_views=None, conditional_highlight=None):

        self.text = text
        self.view = view
        self.args = args or {}
        #self.kwargs = kwargs or {}
        self.icon = icon
        self.permissions = permissions or []
        self.condition = condition
        self.conditional_disable = conditional_disable
        self.description = description
        self.dont_mark_active = dont_mark_active
        self.klass = klass
        self.keep_query = keep_query
        self.conditional_highlight = conditional_highlight  # Used by dynamic sources
        self.children_views = children_views or []
        self.children_classes = children_classes or []
        self.children_url_regex = children_url_regex or []
        self.children_view_regex = children_view_regex or []

    def resolve(self, context, request=None, current_path=None, current_view=None, resolved_object=None):
        # Don't calculate these if passed in an argument
        request = request or Variable('request').resolve(context)
        current_path = current_path or request.META['PATH_INFO']
        current_view = current_view or resolve_to_name(current_path)

        # Preserve unicode data in URL query
        previous_path = smart_unicode(urllib.unquote_plus(smart_str(request.get_full_path()) or smart_str(request.META.get('HTTP_REFERER', u'/'))))
        query_string = urlparse.urlparse(previous_path).query
        parsed_query_string = urlparse.parse_qs(query_string)

        logger.debug('condition: %s', self.condition)

        if resolved_object:
            context['resolved_object'] = resolved_object

        # Check to see if link has conditional display
        if self.condition:
            self.condition_result = self.condition(context)
        else:
            self.condition_result = True

        logger.debug('self.condition_result: %s', self.condition_result)

        if self.condition_result:
            resolved_link = ResolvedLink()
            resolved_link.text = self.text
            resolved_link.icon = self.icon
            resolved_link.permissions = self.permissions
            resolved_link.condition_result = self.condition_result

            try:
                #args, kwargs = resolve_arguments(context, self.get('args', {}))
                args, kwargs = resolve_arguments(context, self.args)
            except VariableDoesNotExist:
                args = []
                kwargs = {}

            if self.view:
                if not self.dont_mark_active:
                    resolved_link.active = self.view == current_view

                try:
                    if kwargs:
                        resolved_link.url = reverse(self.view, kwargs=kwargs)
                    else:
                        resolved_link.url = reverse(self.view, args=args)
                        if self.keep_query:
                            resolved_link.url = u'%s?%s' % (urlquote(resolved_link.url), urlencode(parsed_query_string, doseq=True))

                except NoReverseMatch, exc:
                    resolved_link.url = '#'
                    resolved_link.error = exc
            elif self.url:
                if not self.dont_mark_active:
                    resolved_link.url.active = self.url == current_path

                if kwargs:
                    resolved_link.url = self.url % kwargs
                else:
                    resolved_link.url = self.url % args
                    if self.keep_query:
                        resolved_link.url = u'%s?%s' % (urlquote(resolved_link.url), urlencode(parsed_query_string, doseq=True))
            else:
                resolved_link.active = False

            if self.conditional_highlight:
                resolved_link.active = self.conditional_highlight(context)

            if self.conditional_disable:
                resolved_link.disabled = self.conditional_disable(context)
            else:
                resolved_link.disabled = False

            if current_view in self.children_views:
                resolved_link.active = True

            # TODO: eliminate url_regexes and use new tree base main menu
            for children_view_regex in self.children_view_regex:
                if re.compile(children_view_regex).match(current_view):
                    resolved_link.active = True

            return resolved_link

    @classmethod
    def get_context_navigation_links(cls, context, menu_name=None, links_dict=None):
        request = Variable('request').resolve(context)
        current_path = request.META['PATH_INFO']
        current_view = resolve_to_name(current_path)
        context_links = {}
        if not links_dict:
            links_dict = Link.bound_links

        # Don't fudge with the original global dictionary
        # TODO: fix this
        links_dict = links_dict.copy()

        # Dynamic sources
        # TODO: improve name to 'injected...'
        # TODO: remove, only used by staging files
        try:
            """
            Check for and inject a temporary navigation dictionary
            """
            temp_navigation_links = Variable('temporary_navigation_links').resolve(context)
            if temp_navigation_links:
                links_dict.update(temp_navigation_links)
        except VariableDoesNotExist:
            pass

        # Get view only links
        try:
            view_links = links_dict[menu_name][current_view]['links']
            if view_links:
                context_links.setdefault(None, [])

            for link in view_links:
                context_links[None].append(link.resolve(context, request=request, current_path=current_path, current_view=current_view))
        except KeyError:
            pass

        # Get object links
        for resolved_object, object_properties in get_navigation_objects(context).items():
            # Get object class links
            try:
                object_links = links_dict[menu_name][type(resolved_object)]['links']
                if object_links:
                    context_links.setdefault(resolved_object, [])

                for link in object_links:
                    context_links[resolved_object].append(link.resolve(context, request=request, current_path=current_path, current_view=current_view, resolved_object=resolved_object))
            except KeyError:
                pass

            # Get Combined() instances class links
            try:
                object_links = links_dict[menu_name][Combined(obj=type(resolved_object), view=current_view)]['links']
                if object_links:
                    context_links.setdefault(resolved_object, [])

                for link in object_links:
                    context_links[resolved_object].append(link.resolve(context, request=request, current_path=current_path, current_view=current_view, resolved_object=resolved_object))
            except KeyError:
                pass

        return context_links


class ModelListColumn(object):
    _model_list_columns = {}

    @classmethod
    def get_model(cls, model):
        return cls._model_list_columns.get(model)

    def __init__(self, model, name, attribute):
        self.__class__._model_list_columns.setdefault(model, [])
        self.__class__._model_list_columns[model].extend(columns)


class Combined(object):
    """
    Class that binds a link to a combination of an object and a view.
    This is used to show links relating to a specific object type but only
    in certain views.
    Used by the PageDocument class to show rotatio and zoom link only on
    certain views
    """
    def __init__(self, obj, view):
        self.obj = obj
        self.view = view

    def __hash__(self):
        return hash((self.obj, self.view))

    def __eq__(self, other):
        return hash(self) == hash(other)
