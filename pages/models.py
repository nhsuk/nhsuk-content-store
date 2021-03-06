from django.conf import settings
from django.db import models
from django.http import HttpResponse
from django.shortcuts import redirect
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, MultiFieldPanel, StreamFieldPanel
)
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page as WagtailPage

from nhs_wagtailadmin.views import preview_via_POST_deprecated

from . import components
from .blocks import StreamBlock


class Page(WagtailPage):
    is_creatable = False

    @property
    def description(self):
        return self.search_description

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

    def get_live_children(self):
        return self.get_children().live()

    def get_guide_siblings(self):
        if getattr(self.get_parent().specific, 'guide', False):
            return self.get_siblings().live()
        return []

    class Meta:
        proxy = True


class EditorialPage(Page):
    # META
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
    header = StreamField(
        StreamBlock([
            components.text.as_tuple(),
        ]), verbose_name='Header Content',
        null=True, blank=True
    )

    main = StreamField(
        StreamBlock([
            components.text.as_tuple(),
            components.callout.as_tuple(),
            components.image.as_tuple(),
            components.gallery.as_tuple(),
            components.panel.as_tuple(),
            components.reveal.as_tuple(),
            components.split_content.as_tuple(),
            components.tabs.as_tuple(),
        ]), verbose_name='Main Content',
        null=True, blank=True
    )

    # PANELS
    content_panels = [
        FieldPanel('title'),
        StreamFieldPanel('header'),
        StreamFieldPanel('main'),
    ]

    promote_panels = [
        FieldPanel('non_emergency_callout'),
        FieldPanel('search_description'),
        FieldPanel('choices_origin'),
        FieldPanel('slug'),
    ]

    @property
    def guide(self):
        parent = self.get_parent().specific
        return getattr(parent, 'guide', False)

    # API
    api_fields = [
        'non_emergency_callout', 'choices_origin'
    ]


class FolderPage(Page):
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
        FieldPanel('search_description'),
        FieldPanel('slug'),
    ]
