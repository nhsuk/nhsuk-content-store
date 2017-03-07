from django.contrib.contenttypes.models import ContentType

from pages.models import EditorialPage, FolderPage

from .base import ContentAPIBaseTestCase


class HierarchyBaseTestCase(ContentAPIBaseTestCase):
    def setUp(self):
        """
        Creating the following pages:
            <folder>
                <page1> (live)
                <page2> (live)
                <page3> (not live)
        """
        super().setUp()

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


class ChildrenTestCase(HierarchyBaseTestCase):
    """
    Tests related to the `children` meta field of the Content JSON API Response.
    """

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
        response = self.get_content_api_response(page_id=self.folder.id)
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

        response = self.get_content_api_response(page_id=self.folder.id)
        json_data = response.json()

        self.assertEqual(json_data['meta']['children'], [])


class SiblingsTestCase(HierarchyBaseTestCase):
    """
    Tests related to the `siblings` meta field of the Content JSON API Response.
    """

    def test_siblings_if_parent_is_a_guide(self):
        """
        Tests that the API response of a page with parent.guide == True
        includes siblings:
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
        self.folder.guide = True
        self.folder.save()

        for page in self.live_pages:
            response = self.get_content_api_response(page.id)
            json_data = response.json()

            self.assertEqual(
                [sibling['id'] for sibling in json_data['meta']['siblings']],
                [sibling.id for sibling in self.live_pages]
            )

    def test_no_siblings_if_parent_isnt_a_guide(self):
        """
        Tests that the API response of a page with parent.guide == False
        has empty siblings:
        {
            ...
            meta: {
                siblings: []
            }
        }
        """
        response = self.get_content_api_response(page_id=self.folder.id)
        json_data = response.json()

        self.assertEqual(json_data['meta']['siblings'], [])


class GuideTestCase(HierarchyBaseTestCase):
    """
    Tests related to the `guide` field of the Content JSON API Response.
    """

    def test_guide_folder(self):
        """
        Tests that if <folder>.guide == True
        =>
        all the sub pages will have guide == True as well
        """
        self.folder.guide = True
        self.folder.save()

        for page in self.live_pages + [self.folder]:
            response = self.get_content_api_response(page.id)
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
            response = self.get_content_api_response(page.id)
            json_data = response.json()

            self.assertFalse(json_data['guide'])
