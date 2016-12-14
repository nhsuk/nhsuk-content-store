from .images.views import BakeryImageView
from .pages.views import BakeryPageView

EXPORT_VIEWS = [
    BakeryPageView, BakeryImageView
]


def export(build_dir):
    for view in EXPORT_VIEWS:
        view(build_dir).build_method
