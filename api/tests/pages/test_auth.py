from datetime import timedelta

from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now

from pages.models import EditorialPage

from .base import ContentAPIBaseTestCase


class AuthTestCase(ContentAPIBaseTestCase):
    """
    Tests related to authenticating against the Content API.
    """
    def setUp(self):
        super(AuthTestCase, self).setUp()

        self.page = EditorialPage.objects.create(
            title="Page",
            slug='page',
            content_type=ContentType.objects.get_for_model(EditorialPage),
            path='00010001',
            depth=2,
            numchild=0,
            url_path='/page/',
        )

    def test_401_without_token(self):
        """
        If no token used => 401
        """
        response = self.get_content_api_response(
            self.page.id, auth_headers={}
        )
        self.assertEqual(response.status_code, 401)

    def test_401_with_invalid_token(self):
        """
        If invalid token used => 401
        """
        auth_headers = self.get_auth_header(token='invalid')
        response = self.get_content_api_response(
            self.page.id, auth_headers=auth_headers
        )
        self.assertEqual(response.status_code, 401)

    def test_403_with_token_without_scope(self):
        """
        If token without scope used => 403
        """
        # change scope of the token
        self.nhsuk_frontend_token.scope = ''
        self.nhsuk_frontend_token.save()

        response = self.get_content_api_response(page_id=self.page.id)
        self.assertEqual(response.status_code, 403)

    def test_403_with_token_with_wrong_scope(self):
        """
        If token with wrong scope used => 403
        """
        # change scope of the token
        self.nhsuk_frontend_token.scope = 'write'
        self.nhsuk_frontend_token.save()

        response = self.get_content_api_response(page_id=self.page.id)
        self.assertEqual(response.status_code, 403)

    def test_401_with_expired_token(self):
        """
        If expired token used => 401
        """
        # change scope of the token
        self.nhsuk_frontend_token.expires = now() - timedelta(seconds=1)
        self.nhsuk_frontend_token.save()

        response = self.get_content_api_response(page_id=self.page.id)
        self.assertEqual(response.status_code, 401)

    def test_200_with_right_token(self):
        """
        If write token used => 200
        """
        response = self.get_content_api_response(page_id=self.page.id)
        self.assertEqual(response.status_code, 200)
