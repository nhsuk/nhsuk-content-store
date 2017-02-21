from django import forms
from wagtail.wagtailcore.models import Page

from .actions import Importer
from .utils import get_list_of_children_from_remote


def get_existing_items(item_type):
    """
    Returns the list of slugs for the children of `item_type` (conditions, symptoms).
    """
    parent_page = Page.objects.get(slug=item_type)
    return parent_page.get_children().values_list('slug', flat=True)


class ImportForm(forms.Form):
    conditions = forms.MultipleChoiceField(
        choices=[], required=False,
        widget=forms.CheckboxSelectMultiple
    )
    symptoms = forms.MultipleChoiceField(
        choices=[], required=False,
        widget=forms.CheckboxSelectMultiple
    )

    @classmethod
    def prepare_field(cls, field_name, fields):
        """
        Prepares the field `field_name` with choices from the importable items and
        pre-select the ones not existing in the db already.
        """
        field = fields[field_name]
        importable_items = get_list_of_children_from_remote(field_name)
        existing_items = get_existing_items(field_name)
        field.choices = [
            (item, item) for item in importable_items
        ]
        field.initial = [item for item in importable_items if item not in existing_items]

    def __init__(self, *args, **kwargs):
        self.prepare_field('conditions', self.base_fields)
        self.prepare_field('symptoms', self.base_fields)

        super().__init__(*args, **kwargs)

    def save(self):
        """
        Imports the selected items and returns the list of items that errored.
        """
        importer = Importer(fail_silently=True)

        importer.import_items(
            'conditions', self.cleaned_data['conditions']
        )
        importer.import_items(
            'symptoms', self.cleaned_data['symptoms']
        )

        return importer.items_in_error
