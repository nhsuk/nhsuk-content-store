from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from wagtail.wagtailcore.models import Page

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
        Page.objects.create(
            title="Root",
            slug='root',
            content_type=ContentType.objects.get_for_model(Page),
            path='0001',
            depth=1,
            numchild=1,
            url_path='/',
        )

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
            [child.id for child in self.folder.children()],
            [child.id for child in self.live_pages]
        )

    def test_without_children(self):
        """
        Tests that if there aren't any live sub pages, <page>.children() returns [].
        """
        for page in self.all_pages:
            self.assertEqual(list(page.children()), [])


class SiblingsTestCase(BaseTestCase):
    def test_with_siblings(self):
        """
        Tests that <page>.siblings() returns the list of live siblings.
        """
        for page in self.live_pages:
            self.assertEqual(
                [sibling.id for sibling in page.siblings()],
                [sibling.id for sibling in self.live_pages]
            )

    def test_without_siblings(self):
        """
        Tests that if there aren't any siblings, <page>.siblings() will only include the page itself.
        """
        self.assertEqual(
            [page.id for page in self.folder.siblings()],
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
