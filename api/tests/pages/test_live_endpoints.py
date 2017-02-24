from pages.factories import ConditionPageFactory

from .base import ContentAPIBaseTestCase


class GetByUrlPathTestCase(ContentAPIBaseTestCase):
    """
    Tests getting a page by its path.
    """
    def setUp(self):
        super(GetByUrlPathTestCase, self).setUp()
        self.page = ConditionPageFactory(title='Page')

    def test_get(self):
        """
        Tests that getting a page by its path returns 200 if it exists.
        """
        response = self.get_content_api_response(page_path='conditions/page/')
        self.assertEqual(response.status_code, 200)
        content = response.json()

        self.assertEqual(content['title'], self.page.title)
        self.assertEqual(content['id'], self.page.id)

    def test_404_if_url_doesnt_exist(self):
        """
        Tests that trying to get a page by an invalid page returns 404
        """
        response = self.get_content_api_response(page_path='invalid/')
        self.assertEqual(response.status_code, 404)

    def test_404_if_not_live(self):
        """
        Tests that trying to get a page that is not live returns 404
        """
        self.page.live = False
        self.page.save()

        response = self.get_content_api_response(page_path='conditions/page/')
        self.assertEqual(response.status_code, 404)
