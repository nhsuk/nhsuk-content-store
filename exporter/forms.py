from django import forms

from pages.models import Page

from . import actions


def get_live_pages():
    return Page.objects.live().filter(depth=4).order_by('title').values_list('id', 'title')


class ExportForm(forms.Form):
    pages = forms.MultipleChoiceField(
        choices=get_live_pages, required=False,
        widget=forms.CheckboxSelectMultiple
    )

    def save(self, build_dir):
        actions.export(
            build_dir=build_dir,
            page_ids=self.cleaned_data['pages']
        )
