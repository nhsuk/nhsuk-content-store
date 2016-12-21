from django.templatetags.static import static
from django.utils.html import format_html_join
from wagtail.wagtailadmin.templatetags.wagtailadmin_tags import hook_output
from wagtail.wagtailcore import hooks


@hooks.register('insert_editor_css')
def insert_editor_css():
    css_files = [
        'wagtailmarkdown/css/simplemde.css',
        'wagtailmarkdown/css/simplemde-overrides.css'
    ]
    css_includes = format_html_join(
        '\n',
        '<link rel="stylesheet" href="{0}">',
        ((static(filename),) for filename in css_files),
    )
    return css_includes + hook_output('insert_markdown_editor_css')


@hooks.register('insert_editor_js')
def insert_editor_js():
    js_files = [
        'wagtailmarkdown/js/simplemde.js',
        'wagtailmarkdown/js/simplemde-init.js',
    ]

    js_includes = format_html_join(
        '\n',
        '<script src="{0}"></script>',
        ((static(filename),) for filename in js_files)
    )
    return js_includes + hook_output('insert_markdown_editor_js')
