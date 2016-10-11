from wagtail.wagtailadmin.edit_handlers import BaseFieldPanel


class BaseMarkdownFieldPanel(BaseFieldPanel):
    pass


class MarkdownFieldPanel(object):
    def __init__(self, field_name):
        self.field_name = field_name

    def bind_to_model(self, model):
        return type(str('_MarkdownFieldPanel'), (BaseMarkdownFieldPanel,), {
            'model': model,
            'field_name': self.field_name,
        })
