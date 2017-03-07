from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from home.factories import RootPageFactory
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
        RootPageFactory()

        # create folder
        self.folder = FolderPage.objects.create(
            title="Folder",
            slug='folder',
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


class ChildrenTestCase(BaseTestCase):
    def test_with_children(self):
        """
        Tests that <page>.children() returns the list of live sub pages.
        """
        self.assertEqual(
            [child.id for child in self.folder.get_live_children()],
            [child.id for child in self.live_pages]
        )

    def test_without_children(self):
        """
        Tests that if there aren't any live sub pages, <page>.children() returns [].
        """
        for page in self.all_pages:
            self.assertEqual(list(page.get_live_children()), [])


class SiblingsTestCase(BaseTestCase):
    def test_siblings_if_parent_is_a_guide(self):
        """
        Tests that <page>.get_guide_siblings() returns the list of live siblings if parent.guide == True.
        """
        self.folder.guide = True
        self.folder.save()

        for page in self.live_pages:
            self.assertEqual(
                [sibling.id for sibling in page.get_guide_siblings()],
                [sibling.id for sibling in self.live_pages]
            )

    def test_no_siblings_if_parent_isnt_a_guide(self):
        """
        Tests that <page>.get_guide_siblings() returns [] if parent.guide == False.
        """
        for page in self.live_pages:
            self.assertEqual(page.get_guide_siblings(), [])


class GuideTestCase(BaseTestCase):
    def test_guide_folder(self):
        """
        Tests that if <folder>.guide == True
        =>
        all the sub pages will have guide == True as well
        """
        self.folder.guide = True
        self.folder.save()

        for page in self.all_pages + [self.folder]:
            self.assertTrue(page.guide)

    def test_non_guide_folder(self):
        """
        Tests that if <folder>.guide == False
        =>
        all the sub pages will have guide == False as well
        """
        self.folder.guide = False
        self.folder.save()

        for page in self.all_pages + [self.folder]:
            self.assertFalse(page.guide)
