from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import TestCase
from wagtail.wagtailcore.models import Page, Site

from pages.models import EditorialPage, FolderPage


class BaseTestCase(TestCase):
    def setUp(self):
        """
        Creating the following pages:
            <folder>
                <page1> (live)
                <page2> (live)
                <page3> (not live)
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

        # create guide folder
        self.folder = FolderPage.objects.create(
            title="Folder",
            slug='guide',
            content_type=ContentType.objects.get_for_model(FolderPage),
            path='00010001',
            depth=2,
            numchild=3,
            guide=False,
            url_path='/folder/',
        )

        # create sub pages
        self.page1 = EditorialPage.objects.create(
            title="Page 1",
            slug='page-1',
            content_type=ContentType.objects.get_for_model(EditorialPage),
            path='000100010001',
            depth=3,
            numchild=0,
            url_path='/folder/page-1/',
        )
        self.page2 = EditorialPage.objects.create(
            title="Page 2",
            slug='page-2',
            content_type=ContentType.objects.get_for_model(EditorialPage),
            path='000100010002',
            depth=3,
            numchild=0,
            url_path='/folder/page-2/',
        )
        self.page3 = EditorialPage.objects.create(
            title="Page 3",
            slug='page-3',
            content_type=ContentType.objects.get_for_model(EditorialPage),
            path='000100010003',
            depth=3,
            numchild=0,
            url_path='/folder/page-3/',
            live=False
        )

        self.live_pages = [self.page1, self.page2]
        self.all_pages = [self.page1, self.page2, self.page3]

    def get_response(self, page_id, **params):
        return self.client.get(reverse('wagtailapi:pages:detail', args=(page_id, )), params)


class ChildrenTestCase(BaseTestCase):
    def test_folder(self):
        """
        Tests that the API response of the folder page is:
        {
            ...
            meta: {
                children: [
                    {
                        ...
                    },
                    {
                        ...
                    }
                ]
            }
        }
        """
        response = self.get_response(self.folder.id)
        json_data = response.json()

        children_data = json_data['meta']['children']
        self.assertEqual(
            [data['id'] for data in children_data],
            [page.id for page in self.live_pages]
        )

    def test_empty_folder(self):
        """
        Tests that the children field of the API response is [] in case of no live children.
        {
            ...
            meta: {
                children: []
            }
        }
        """
        self.page1.live = False
        self.page1.save()

        self.page2.delete()

        response = self.get_response(self.folder.id)
        json_data = response.json()

        self.assertEqual(json_data['meta']['children'], [])


class SiblingsTestCase(BaseTestCase):
    def test_with_siblings(self):
        """
        Tests that the API response of a page with siblings is:
        {
            ...
            meta: {
                siblings: [
                    {
                        ...
                    },
                    {
                        ...
                    }
                ]
            }
        }
        """
        for page in self.live_pages:
            response = self.get_response(page.id)
            json_data = response.json()

            self.assertEqual(
                [sibling['id'] for sibling in json_data['meta']['siblings']],
                [sibling.id for sibling in self.live_pages]
            )

    def test_without_siblings(self):
        """
        Tests that the API response of a page without siblings only include the page itself:
        {
            ...
            meta: {
                siblings: [{
                    ...
                }]
            }
        }
        """
        response = self.get_response(self.folder.id)
        json_data = response.json()

        self.assertEqual(
            [data['id'] for data in json_data['meta']['siblings']],
            [self.folder.id]
        )


class GuideTestCase(BaseTestCase):
    def test_guide_folder(self):
        """
        Tests that if <folder>.guide == True
        =>
        all the sub pages will have guide == True as well
        """
        self.folder.guide = True
        self.folder.save()

        for page in self.live_pages + [self.folder]:
            response = self.get_response(page.id)
            json_data = response.json()

            self.assertTrue(json_data['guide'])

    def test_non_guide_folder(self):
        """
        Tests that if <folder>.guide == False
        =>
        all the sub pages will have guide == False as well
        """
        self.folder.guide = False
        self.folder.save()

        for page in self.live_pages + [self.folder]:
            response = self.get_response(page.id)
            json_data = response.json()

            self.assertFalse(json_data['guide'])
