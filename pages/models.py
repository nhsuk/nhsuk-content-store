from django.conf import settings
from django.db import models
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, MultiFieldPanel, StreamFieldPanel
)
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page as WagtailPage

from nhs_wagtailadmin.views import preview_via_POST_deprecated

from .blocks import StreamBlock
from .page_elements import Components


class Page(WagtailPage):
    is_creatable = False

    def serve(self, request, *args, **kwargs):
        """
        Redirects to the live frontend version of this page.
        """
        if not settings.FRONTEND_BASE_URL:
            return HttpResponse('Please set FRONTEND_BASE_URL in your settings.py')

        site_id, root_path, root_url = self.get_url_parts()
        return redirect('{}{}'.format(settings.FRONTEND_BASE_URL, root_url))

    def serve_preview(self, request, mode_name):
        preview_via_POST_deprecated()

    class Meta:
        proxy = True


class ChildrenSiblingsMixin(object):
    def children(self):
        return self.get_children().live()

    def siblings(self):
        return self.get_siblings().live()


class EditorialPage(ChildrenSiblingsMixin, Page):
    SIDEBAR_ORDER_LAST = 'last'
    SIDEBAR_ORDER_FIRST = 'first'
    SIDEBAR_ORDER_CHOICES = (
        (SIDEBAR_ORDER_LAST, 'Last'),
        (SIDEBAR_ORDER_FIRST, 'First'),
    )

    # META
    sidebar_order = models.CharField(
        max_length=50,
        choices=SIDEBAR_ORDER_CHOICES,
        default=SIDEBAR_ORDER_LAST
    )
    non_emergency_callout = models.BooleanField(
        default=True,
        verbose_name='Non-emergency callout',
        help_text='Shows/hides the call 111 section'
    )
    choices_origin = models.CharField(
        max_length=255, blank=True,
        help_text=(
            'Optional. Related Choices page '
            '(e.g. conditions/stomach-ache-abdominal-pain/Pages/Introduction.aspx)'
        )
    )

    # CONTENT BLOCKS
    before = StreamField(
        StreamBlock([
            Components.get('markdown'),
            Components.get('figureList'),
        ]), null=True, blank=True
    )

    local_header = StreamField(
        StreamBlock([
            Components.get('markdown'),
            Components.get('sectionNav'),
        ]), null=True, blank=True
    )

    main = StreamField(
        StreamBlock([
            Components.get('markdown'),
            Components.get('sectionList'),
        ]), null=True, blank=True
    )

    sidebar = StreamField(
        StreamBlock([
            Components.get('markdown'),
        ]), null=True, blank=True
    )

    # PANELS
    content_panels = [
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('sidebar_order'),
        ]),
        StreamFieldPanel('local_header'),
        StreamFieldPanel('before'),
        StreamFieldPanel('main'),
        StreamFieldPanel('sidebar')
    ]

    promote_panels = [
        MultiFieldPanel([
            FieldPanel('non_emergency_callout'),
            FieldPanel('choices_origin'),
        ]),
        MultiFieldPanel([
            FieldPanel('slug'),
            FieldPanel('seo_title'),
            FieldPanel('search_description'),
        ], ugettext_lazy('Common page configuration')),
    ]

    @property
    def guide(self):
        parent = self.get_parent().specific
        return getattr(parent, 'guide', False)

    # API
    api_fields = [
        'sidebar_order', 'non_emergency_callout', 'choices_origin',
        'local_header', 'before', 'main', 'sidebar', 'guide'
    ]
    api_meta_fields = [
        'children', 'siblings'
    ]


class FolderPage(ChildrenSiblingsMixin, Page):
    guide = models.BooleanField(
        default=False,
        help_text='If ticked, all its sub-pages will be part of this guide'
    )

    # PANELS
    content_panels = [
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('guide'),
        ]),
    ]

    promote_panels = [
        MultiFieldPanel([
            FieldPanel('slug'),
        ], ugettext_lazy('Common page configuration')),
    ]

    # API
    api_fields = [
        'guide'
    ]
    api_meta_fields = [
        'children', 'siblings'
    ]
