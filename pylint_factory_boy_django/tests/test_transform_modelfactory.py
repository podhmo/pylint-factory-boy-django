# -*- coding:utf-8 -*-
import unittest

"""
from <app> import models
from <app> import models as _models
from <app>.models import User
"<app>._models.User"

"""

@unittest.skip("")
class ModelFactoryPaddingOldStyleTests(unittest.TestCase):
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

    def test_it__oldstyle3(self):
        code = """\
from pylint_factory_boy_django import models as m
from fuctory.django import DjangoModelFactory

class UserFactory(DjangoModelFactory):
    FACTORY_FOR = m.User
"""
        ast = self._callFUT(code)
        self.assertTrue(ast["UserFactory"]["name"])

    def test_it__oldstyle4(self):
        code = """\
from pylint_factory_boy_django.models import User as Foo
from fuctory.django import DjangoModelFactory

class UserFactory(DjangoModelFactory):
    FACTORY_FOR = Foo
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


class ModelFactoryPaddingNewStyleTests(unittest.TestCase):
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

    def test_it__newstyle(self):
        code = """\
from pylint_factory_boy_django import models
from fuctory.django import DjangoModelFactory

class UserFactory(DjangoModelFactory):
    class Meta:
        model = models.User
"""
        ast = self._callFUT(code)
        self.assertTrue(ast["UserFactory"]["name"])

    def test_it__newstyle2(self):
        code = """\
from pylint_factory_boy_django.models import User
from fuctory.django import DjangoModelFactory

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
"""
        ast = self._callFUT(code)
        self.assertTrue(ast["UserFactory"]["name"])

    def test_it__newstyle3(self):
        code = """\
from pylint_factory_boy_django import models as m
from fuctory.django import DjangoModelFactory

class UserFactory(DjangoModelFactory):
    class Meta:
        model = m.User
"""
        ast = self._callFUT(code)
        self.assertTrue(ast["UserFactory"]["name"])

    def test_it__newstyle4(self):
        code = """\
from pylint_factory_boy_django.models import User as Foo
from fuctory.django import DjangoModelFactory

class UserFactory(DjangoModelFactory):
    class Meta:
        model = Foo
"""
        ast = self._callFUT(code)
        self.assertTrue(ast["UserFactory"]["name"])
