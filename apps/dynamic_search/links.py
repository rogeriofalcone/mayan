from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.classes import Link

from .icons import icon_search

search = Link(text=_(u'search'), view='search', icon=icon_search)
search_advanced = Link(text=_(u'advanced search'), view='search_advanced', icon=icon_search) # TODO: make different icon
search_again = Link(text=_(u'search again'), view='search_again', icon=icon_search) # TODO: make different icon
