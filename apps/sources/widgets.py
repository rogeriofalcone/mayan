from __future__ import absolute_import

from django import forms
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from .icons import icon_cross
from .literals import SOURCE_ICON_ICON


class IconRadioFieldRenderer(forms.widgets.RadioFieldRenderer):
    def render(self):
        results = []
        results.append(u'<ul>\n')
        for option in self:
            if option.choice_value:
                icon = SOURCE_ICON_ICON[option.choice_value]
            else:
                icon = icon_cross
            results.append(u'<li class="undecorated_list">%s%s</li>' % (icon.display_small(), force_unicode(option)))

        results.append(u'\n</ul>')
        return mark_safe(u'\n'.join(results))


class IconRadioSelect(forms.widgets.RadioSelect):
    renderer = IconRadioFieldRenderer


def staging_file_thumbnail(staging_file):
    try:
        staging_file.get_valid_image()
        template = u'<a class="fancybox-staging" href="%(url)s" title="%(filename)s" rel="staging")><img class="lazy-load-interactive" data-src="%(thumbnail)s" src="%(static_url)simages/ajax-loader.gif" alt="%(string)s" /><noscript><img src="%(thumbnail)s" alt="%(string)s" /></noscript></a>'
    except:
        template = u'<img class="lazy-load-interactive" data-src="%(thumbnail)s" src="%(static_url)simages/ajax-loader.gif" alt="%(string)s" /><noscript><img src="%(thumbnail)s" alt="%(string)s" /></noscript>'

    return mark_safe(template % {
        'url': reverse('staging_file_preview', args=[staging_file.source.source_type, staging_file.source.pk, staging_file.id]),
        'thumbnail': reverse('staging_file_thumbnail', args=[staging_file.source.pk, staging_file.id]),
        'static_url': settings.STATIC_URL,
        'string': _(u'thumbnail'),
        'filename': staging_file.filename
    })
