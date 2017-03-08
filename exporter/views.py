import os
import tempfile
import zipfile

from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import render

from .forms import ExportForm

ZIP_ROOT_DIR = 'content'


def export_content(request):
    if request.method == 'POST':
        form = ExportForm(request.POST)
        if form.is_valid():
            # export to temp folder
            exported_content = tempfile.mkdtemp()
            form.save(build_dir=exported_content)

            # create the zip file
            temp_file = ContentFile(''.encode("latin-1"), name=ZIP_ROOT_DIR)
            with zipfile.ZipFile(temp_file, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
                for root_dir, _, files in os.walk(exported_content):
                    for filename in files:
                        # path to the file in the filesystem
                        file_path = os.path.join(root_dir, filename)

                        # path to the file in the zip file
                        zip_path = os.path.join(
                            ZIP_ROOT_DIR,
                            root_dir.split(exported_content)[1][1:],
                            filename
                        )

                        zf.write(file_path, zip_path)

            # Grab ZIP file from in-memory, make response with correct MIME-type
            response = HttpResponse(temp_file, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=%s.zip' % ZIP_ROOT_DIR

            return response
    else:
        form = ExportForm()

    return render(
        request,
        'exporter/export_form.html', {
            'form': form
        }
    )
