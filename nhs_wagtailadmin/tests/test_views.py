from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings
from wagtail.tests.utils import WagtailTestUtils

from nhs_wagtailadmin.exceptions import DeprecatedException
from nhs_wagtailadmin.views import generate_preview_signature
from pages.factories import ConditionPageFactory


class GeneratePreviewSignatureTestCase(TestCase):

    @override_settings(PREVIEW_SIGNATURE_KEY='test')
    def test_with_default_key(self):
        """
        Tests that if no `key` param is specified, the default settings.PREVIEW_SIGNATURE_KEY
        is used.
        """
        self.assertEqual(
            generate_preview_signature(11, 34),
            b'48L1QPVKvG0uTmvOR3YRKK3guzQ='
        )

    @override_settings(PREVIEW_SIGNATURE_KEY='test')
    def test_with_given_key(self):
        """
        Tests that you can specify a different key using the param `key`.
        """
        self.assertEqual(
            generate_preview_signature(11, 34, key='another-key'),
            b'M-2cf8_5ZMXrM6olfFqpHs1-ZBs='
        )


class PreviewViaPOSTdeprecatedTestCase(TestCase, WagtailTestUtils):
    """
    Tests that deprecated views raise a DeprecatedException to make it
    obvious that they shouldn't be called.
    """

    def setUp(self):
        self.user = self.login()

    def test_preview_on_add(self):
        url = reverse('wagtailadmin_pages:preview_on_add', args=('tests', 'simplepage', 1))
        self.assertRaises(
            DeprecatedException, self.client.post, url, {}
        )

    def test_preview_on_edit(self):
        url = reverse('wagtailadmin_pages:preview_on_edit', args=(1, ))
        self.assertRaises(
            DeprecatedException, self.client.post, url, {}
        )

    def test_preview(self):
        url = reverse('wagtailadmin_pages:preview')
        self.assertRaises(
            DeprecatedException, self.client.post, url, {}
        )

    def test_preview_loading(self):
        url = reverse('wagtailadmin_pages:preview_loading')
        self.assertRaises(
            DeprecatedException, self.client.post, url, {}
        )


class BaseRevisionPreviewTestCase(TestCase, WagtailTestUtils):
    def setUp(self):
        # set permissions
        wagtailadmin_content_type, _ = ContentType.objects.get_or_create(
            app_label='wagtailadmin',
            model='admin'
        )
        Permission.objects.get_or_create(
            content_type=wagtailadmin_content_type,
            codename='access_admin',
            name='Can access Wagtail admin'
        )

        # login
        self.user = self.login()

        # create pages
        self.page = ConditionPageFactory(title='Page')
        self.revision = self.page.save_revision()


class ViewDraftTestCase(BaseRevisionPreviewTestCase):
    def get_url(self, page_id):
        return reverse('wagtailadmin_pages:view_draft', args=(page_id, ))

    def test_redirects_to_login_if_not_logged_in(self):
        """
        Tests that it redirects to the admin login page if the user is not logged in.
        """
        self.client.logout()

        url = self.get_url(page_id=1)
        response = self.client.get(url)
        self.assertRedirects(response, reverse('wagtailadmin_login') + '?next=' + url)

    def test_view(self):
        """
        Tests that it redirects to the revision view with the latest revision as param.
        """
        response = self.client.get(self.get_url(page_id=self.page.id))

        self.assertRedirects(
            response,
            reverse('wagtailadmin_pages:revisions_view', args=(self.page.id, self.revision.id)),
            target_status_code=302
        )

    def test_404_if_page_doesnt_exist(self):
        """
        Tests that it returns 404  if the page does not exist
        """
        url = self.get_url(page_id=self.page.id + 1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class PreviewForModerationTestCase(BaseRevisionPreviewTestCase):
    def setUp(self):
        super(PreviewForModerationTestCase, self).setUp()

        # mark the revision as awaiting moderation
        self.revision.submitted_for_moderation = True
        self.revision.save()

    def get_url(self, revision_id):
        return reverse('wagtailadmin_pages:preview_for_moderation', args=(revision_id, ))

    def test_redirects_to_login_if_not_logged_in(self):
        """
        Tests that it redirects to the admin login page if the user is not logged in.
        """
        self.client.logout()

        url = self.get_url(revision_id=1)
        response = self.client.get(url)
        self.assertRedirects(response, reverse('wagtailadmin_login') + '?next=' + url)

    def test_view(self):
        """
        Tests that it redirects to the revision view.
        """
        url = self.get_url(revision_id=self.revision.id)
        response = self.client.get(url)

        self.assertRedirects(
            response,
            reverse('wagtailadmin_pages:revisions_view', args=(self.page.id, self.revision.id)),
            target_status_code=302
        )

    def test_403_if_user_cant_publish(self):
        """
        Tests that a user without perms would get a 403.
        """
        # user can access the admin panel but doesn't have publishing permissions
        self.user.is_superuser = False
        self.user.user_permissions.add(
            Permission.objects.get(content_type__app_label='wagtailadmin', codename='access_admin')
        )
        self.user.save()

        url = self.get_url(revision_id=self.revision.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_redirects_if_revision_not_awaiting_moderation(self):
        """
        Tests that if the revision is not awaiting moderation, the view returns an error msg.
        """
        self.revision.submitted_for_moderation = False
        self.revision.save()

        url = self.get_url(revision_id=self.revision.id)
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, reverse('wagtailadmin_home'))
        self.assertContains(response, 'is not currently awaiting moderation')

    def test_404_if_revision_doesnt_exist(self):
        """
        Tests that it returns 404 if the revision doesn't exist.
        """
        url = self.get_url(revision_id=self.revision.id + 1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class RevisionViewTestCase(BaseRevisionPreviewTestCase):

    def get_url(self, page_id, revision_id):
        return reverse('wagtailadmin_pages:revisions_view', args=(page_id, revision_id, ))

    def test_redirects_to_login_if_not_logged_in(self):
        """
        Tests that it redirects to the admin login page if the user is not logged in.
        """
        self.client.logout()

        url = self.get_url(page_id=1, revision_id=1)
        response = self.client.get(url)
        self.assertRedirects(response, reverse('wagtailadmin_login') + '?next=' + url)

    @override_settings(
        FRONTEND_PREVIEW_URL='http://example.com/preview/{signature}/{page_id}/{revision_id}',
        PREVIEW_SIGNATURE_KEY='test'
    )
    def test_view(self):
        """
        Tests that it redirects to settings.FRONTEND_PREVIEW_URL with related signature, page id and revision id.
        """
        url = self.get_url(page_id=self.page.id, revision_id=self.revision.id)
        response = self.client.get(url)
        self.assertEqual(
            response.url,
            'http://example.com/preview/{}/{}/{}'.format(
                generate_preview_signature(self.page.id, self.revision.id).decode(),
                self.page.id, self.revision.id
            )
        )

    @override_settings(FRONTEND_PREVIEW_URL=None)
    def test_FRONTEND_PREVIEW_URL_not_set(self):
        """
        Tests that if settings.FRONTEND_PREVIEW_URL is not set, it returns a msg asking you to do so.
        """
        url = self.get_url(page_id=self.page.id, revision_id=self.revision.id)
        response = self.client.get(url)
        self.assertContains(response, 'Please set FRONTEND_PREVIEW_URL in your settings.py')

    def test_404_if_page_doesnt_exist(self):
        """
        Tests that it returns 404 if the page doesn't exist.
        """
        url = self.get_url(page_id=self.page.id + 1, revision_id=self.revision.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_404_if_revision_doesnt_exist(self):
        """
        Tests that it returns 404 if the page doesn't exist.
        """
        url = self.get_url(page_id=self.page.id, revision_id=self.revision.id + 1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
