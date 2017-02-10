from django.shortcuts import render
from wagtail.wagtailadmin import messages

from .forms import ImportForm


def import_content(request):
    saved = False
    items_in_error = []
    if request.method == 'POST':
        form = ImportForm(request.POST)
        if form.is_valid():
            items_in_error = form.save()
            messages.success(request, "Content imported")
            saved = True
    else:
        form = ImportForm()

    return render(
        request,
        'importer/import_form.html', {
            'form': form,
            'saved': saved,
            'items_in_error': items_in_error
        }
    )
