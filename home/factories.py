import factory
from django.core.exceptions import ObjectDoesNotExist

from pages.models import Page

from . import models


class ParentBasedFactory(object):
    _ParentFactory = None
    _unique = False

    @classmethod
    def create_if_necessary(cls, *args, **kwargs):
        parent = None
        if cls._ParentFactory:
            parent = cls._ParentFactory.create_if_necessary()

        obj = None
        created = False
        if cls._unique:
            try:
                obj = cls._meta.model.objects.get(slug=cls.slug)
            except ObjectDoesNotExist:
                pass

        if not obj:
            obj = super().create(*args, **kwargs)
            created = True

        if parent and created:
            parent.numchild = parent.numchild + 1
            parent.save()

        return obj

    @classmethod
    def create(cls, *args, **kwargs):
        return cls.create_if_necessary(*args, **kwargs)


class RootPageFactory(ParentBasedFactory, factory.django.DjangoModelFactory):
    title = 'Root'
    slug = 'root'
    path = '0001'
    depth = 1

    _unique = True

    class Meta:
        model = Page


class HomePageFactory(ParentBasedFactory, factory.django.DjangoModelFactory):
    title = 'Home'
    slug = 'home'
    path = '00010001'
    depth = 2

    _ParentFactory = RootPageFactory
    _unique = True

    class Meta:
        model = models.HomePage
