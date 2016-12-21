import os
import tempfile
import zipfile

from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.six import b

from . import actions

ZIP_ROOT_DIR = "content"


def export_content(request):
    if request.method == 'POST':
        exported_content = tempfile.mkdtemp()

        actions.export(build_dir=exported_content)

        temp_file = ContentFile(b(""), name=ZIP_ROOT_DIR)
        with zipfile.ZipFile(temp_file, "w", compression=zipfile.ZIP_DEFLATED) as zf:
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
        return render(request, 'exporter/export_form.html')
