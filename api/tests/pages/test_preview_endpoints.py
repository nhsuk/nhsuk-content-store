from django.contrib.contenttypes.models import ContentType
from wagtail.wagtailcore.models import PageRevision

from home.models import HomePage
from pages.models import EditorialPage

from .base import ContentAPIBaseTestCase


class PreviewPagesTestCase(ContentAPIBaseTestCase):
    """
    Tests getting the content of a page by its revision id.
    """

    def setUp(self):
        super(PreviewPagesTestCase, self).setUp()

        self.home = HomePage.objects.create(
            title='Homepage',
            slug='home',
            content_type=ContentType.objects.get_for_model(HomePage),
            path='00010001',
            depth=2,
            numchild=1,
            url_path='/home/',

        )
        self.page = EditorialPage.objects.create(
            title='Page',
            slug='page',
            content_type=ContentType.objects.get_for_model(EditorialPage),
            path='000100010001',
            depth=3,
            numchild=0,
            url_path='/home/page/',
            live=True
        )

    def test_get_by_revision_x(self):
        """
        Tests that getting a page by its revision id returns the related content, not the live one.
        """

        # save some revisions
        revision_data = []
        for change_number in range(1, 3):
            self.page.title = 'Page change {}'.format(change_number)
            self.page.save()
            revision = self.page.save_revision()
            revision_data.append(
                (revision.id, self.page.title)
            )

        # get those versions and check that page.title == saved title
        for revision_id, page_title in revision_data:
            response = self.get_preview_content_api_response(self.page.id, revision_id=revision_id)
            content = response.json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(content['title'], page_title)

    def test_404_if_revision_doesnt_exist(self):
        """
        Tests that trying to get a page by an invalid revision returns 404.
        """
        # save a few revisions
        for change_number in range(1, 3):
            self.page.title = 'Page change {}'.format(change_number)
            self.page.save()
            self.page.save_revision()

        # get invalid revision id (last id + 1)
        revision_id = PageRevision.objects.order_by('-id')[0].id + 1

        response = self.get_preview_content_api_response(self.page.id, revision_id=revision_id)
        self.assertEqual(response.status_code, 404)

    def test_get_defaults_to_latest_revision(self):
        """
        Tests that getting a page without specifying a revision id returns the latest version.
        """
        # save some revisions
        latest_title = self.page.title
        for change_number in range(1, 3):
            self.page.title = 'Page change {}'.format(change_number)
            self.page.save()
            self.page.save_revision()
            latest_title = self.page.title

        # check that returned content.title == latest title
        response = self.get_preview_content_api_response(self.page.id)
        content = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['title'], latest_title)
