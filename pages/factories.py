import factory

from home.factories import HomePageFactory, ParentBasedFactory

from . import models


class ConditionsPageFactory(ParentBasedFactory, factory.django.DjangoModelFactory):
    title = 'Conditions'
    slug = 'conditions'
    path = '000100010002'
    depth = 3

    _ParentFactory = HomePageFactory
    _unique = True

    class Meta:
        model = models.FolderPage


class ConditionPageFactory(ParentBasedFactory, factory.django.DjangoModelFactory):
    path = factory.Sequence(lambda n: '000100010002%04d' % (n + 1))
    depth = 4

    _ParentFactory = ConditionsPageFactory
    _unique = False

    class Meta:
        model = models.EditorialPage


class SymptomsPageFactory(ParentBasedFactory, factory.django.DjangoModelFactory):
    title = 'Symptoms'
    slug = 'symptoms'
    path = '000100010001'
    depth = 3

    _ParentFactory = HomePageFactory
    _unique = True

    class Meta:
        model = models.FolderPage


class SymptomPageFactory(ParentBasedFactory, factory.django.DjangoModelFactory):
    path = factory.Sequence(lambda n: '000100010001%04d' % (n + 1))
    depth = 4

    _ParentFactory = SymptomsPageFactory
    _unique = False

    class Meta:
        model = models.EditorialPage


class ConditionFolderPageFactory(ParentBasedFactory, factory.django.DjangoModelFactory):
    path = factory.Sequence(lambda n: '000100010002%04d' % (n + 1))
    depth = 4

    _ParentFactory = ConditionsPageFactory
    _unique = False

    class Meta:
        model = models.FolderPage
