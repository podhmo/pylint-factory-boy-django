# -*- coding:utf-8 -*-
import unittest

"""
_models as models;
_models
_models. import User
"pylint_factory_boy_django._models.User"
"""


class Tests(unittest.TestCase):
    def _makeManager(self):
        from astroid.manager import AstroidManager
        return AstroidManager()

    def _makeBuilder(self, manager):
        from astroid.builder import AstroidBuilder
        return AstroidBuilder(manager)

    def _callFUT(self, code):
        from pylint_factory_boy_django.transforms import modelfactory
        manager = self._makeManager()
        modelfactory.register_transform(manager)
        builder = self._makeBuilder(manager)
        return builder.string_build(code)

    def test_it__oldstyle(self):
        code = """\
from pylint_factory_boy_django import models
from fuctory.django import DjangoModelFactory

class UserFactory(DjangoModelFactory):
    FACTORY_FOR = models.User
"""
        ast = self._callFUT(code)
        self.assertTrue(ast["UserFactory"]["name"])

    def test_it__oldstyle2(self):
        code = """\
from pylint_factory_boy_django.models import User
from fuctory.django import DjangoModelFactory

class UserFactory(DjangoModelFactory):
    FACTORY_FOR = User
"""
        ast = self._callFUT(code)
        self.assertTrue(ast["UserFactory"]["name"])

    def test_it__oldstyle_string(self):
        code = """\
from fuctory.django import DjangoModelFactory

class UserFactory(DjangoModelFactory):
    FACTORY_FOR = "pylint_factory_boy_django.models.User"
"""
        ast = self._callFUT(code)
        self.assertTrue(ast["UserFactory"]["name"])
