import json
import os

from django.core.management.base import BaseCommand

from pages.models import EditorialPage, FolderPage


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        conditions_filepath = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'conditions.json'
        )
        with open(conditions_filepath, 'r') as f:
            conditions = json.loads(f.read())

            conditions_folder = FolderPage.objects.get(slug='conditions')

            for condition in conditions:
                new_page = EditorialPage(
                    title=condition
                )
                conditions_folder.add_child(instance=new_page)

                new_page.save_revision()

        print('Finished...')
