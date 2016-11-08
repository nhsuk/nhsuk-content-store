from datetime import timedelta

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.timezone import now
from oauth2_provider.compat import get_user_model
from oauth2_provider.models import AccessToken, get_application_model
from wagtail.wagtailcore.models import Page, Site

Application = get_application_model()
UserModel = get_user_model()


class ContentAPIBaseTestCase(TestCase):
    """
    TestCase superclass for testing content api related logic.
    It includes the logic necessary to authenticate requests.
    """

    def setUpAuthData(self):
        """
        Creates User, Application and Access Token for authenticating against the content api.
        """
        self.nhsuk_frontend_user = UserModel.objects.create_user("nhsuk-frontend-user")

        self.nhsuk_frontend_application = Application(
            name="Test NHS.UK Frontend Application",
            user=self.nhsuk_frontend_user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS,
        )
        self.nhsuk_frontend_application.save()
        self.nhsuk_frontend_token = AccessToken.objects.create(
            user=self.nhsuk_frontend_user,
            token='tokstr',
            application=self.nhsuk_frontend_application,
            expires=now() + timedelta(days=365),
            scope='read'
        )

    def setUpPages(self):
        """
        Creates the root Page and the default Site.
        """
        root = Page.objects.create(
            title="Root",
            slug='root',
            content_type=ContentType.objects.get_for_model(Page),
            path='0001',
            depth=1,
            numchild=1,
            url_path='/',
        )
        Site.objects.create(hostname='localhost', root_page=root, is_default_site=True)

    def setUp(self):
        super(ContentAPIBaseTestCase, self).setUp()
        self.setUpAuthData()
        self.setUpPages()

    def get_auth_header(self, token):
        return {
            'HTTP_AUTHORIZATION': 'Bearer ' + token,
        }

    def get_content_api_response(self, page_id, auth_headers=None):
        """
        Can be used to request the page with id == `page_id` with the
        given `auth_headers` or the default one not specified.
        """
        if auth_headers is None:
            auth_headers = self.get_auth_header(
                self.nhsuk_frontend_token.token
            )
        url = reverse('wagtailapi:pages:detail', args=(page_id, ))
        return self.client.get(url, **auth_headers)
