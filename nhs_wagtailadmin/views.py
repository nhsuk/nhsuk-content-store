import base64
import hashlib
import hmac

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.six import text_type
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_GET
from wagtail.wagtailadmin import messages
from wagtail.wagtailcore.models import Page, PageRevision

from .exceptions import DeprecatedException


def generate_preview_signature(page_id, revision_id, key=None):
    """
    Generates a signature to be used when previewing a revision.
    It uses an SHA1 HMAC(K, m) where:
        - K: a private key shared with the frontend app
        - m: is the message '<page-id>/<revision-id>/'
    """
    if not key:
        key = settings.PREVIEW_SIGNATURE_KEY

    # Key must be a bytes object
    if isinstance(key, text_type):
        key = key.encode()

    url = '{}/{}/'.format(page_id, revision_id)
    return base64.urlsafe_b64encode(
        hmac.new(key, url.encode(), hashlib.sha1).digest()
    )


@require_GET
def revisions_view(request, page_id, revision_id):
    """
    Redirects to a frontend preview page of type:
        `<frontend-preview-url>/<signature>/<page-id>/<revision-id>`
    Where:
        - frontend-preview-url: settings.FRONTEND_PREVIEW_URL
        - signature: see the generate_preview_signature method
        - page-id: id of the page
        - revision-id: id of the revision
    """
    if not settings.FRONTEND_PREVIEW_URL:
        return HttpResponse(_('Please set FRONTEND_PREVIEW_URL in your settings.py'))

    page = get_object_or_404(Page, id=page_id).specific
    revision = get_object_or_404(page.revisions, id=revision_id)
    signature = generate_preview_signature(page.id, revision.id)

    return redirect(
        settings.FRONTEND_PREVIEW_URL.format(
            signature=signature.decode(),
            page_id=page.id,
            revision_id=revision.id
        )
    )


@require_GET
def view_draft(request, page_id):
    """
    Redirects to revisions_view using the latest revision of the page with id == `page_id`.
    """
    page = get_object_or_404(Page, id=page_id)
    revision = page.get_latest_revision()

    return redirect('wagtailadmin_pages:revisions_view', page.id, revision.id)


@require_GET
def preview_for_moderation(request, revision_id):
    """
    Checks that the revision is awating moderation and if so, redirects to revisions_view.
    """
    revision = get_object_or_404(PageRevision, id=revision_id)
    if not revision.page.permissions_for_user(request.user).can_publish():
        raise PermissionDenied

    if not revision.submitted_for_moderation:
        messages.error(request, _("The page '{0}' is not currently awaiting moderation.").format(revision.page.title))
        return redirect('wagtailadmin_home')

    return redirect('wagtailadmin_pages:revisions_view', revision.page.id, revision.id)


def preview_via_POST_deprecated(*args, **kwargs):
    """
    Previewing a page using the default Wagtail logic is deprecated.

    The current logic requires saving the revision and previewing it using
    `nhs_wagtailadmin.views.revisions_view`.
    """

    raise DeprecatedException(
        'This view has been deprecated in NHS.UK. '
        'Please use nhs_wagtailadmin.views.revisions_view instead'
    )
