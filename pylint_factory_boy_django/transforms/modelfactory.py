# -*- coding:utf-8 -*-
import os.path
from astroid import MANAGER
from astroid.builder import AstroidBuilder
from astroid.exceptions import UnresolvableName
from astroid.node_classes import Getattr, Const
# from astroid.as_string import to_code
from astroid import scoped_nodes
from weakref import WeakKeyDictionary, WeakValueDictionary
from importlib import find_loader


class FindModuleError(Exception):
    pass


class FromStmtImportedCache(object):
    def __init__(self, builder=None):
        self.from_stmt_cache = WeakKeyDictionary()
        self.modules = WeakValueDictionary()
        self.builder = builder or AstroidBuilder(MANAGER)

    def register_from_stmt(self, module, from_stmt):
        self.from_stmt_cache.setdefault(module, []).append(from_stmt)

    def get_symbol_from_stmt(self, parent, target_name):
        for stmt in self.from_stmt_cache[parent]:
            for name, bound in stmt.names:
                if target_name == name or target_name == bound:
                    try:
                        module = self.get_module(stmt.modname)
                    except FindModuleError:
                        module = self.get_module(*stmt.modname.rsplit(".", 1))
                    try:
                        # member of module(e.g. from unittest.mock import patch)
                        return module[name]
                    except KeyError:
                        # not member of module(e.g. from unittest import mock)
                        return self.get_module(stmt.modname, extraname=name)

    def get_module(self, modulename, extraname=None):
        if extraname is not None:
            fullname = ".".join([modulename, extraname])
        else:
            fullname = modulename

        if fullname in self.modules:
            return self.modules[fullname]

        try:
            path = find_loader(fullname).path
        except AttributeError:
            if modulename == fullname:
                raise FindModuleError
            # this is django.db.models or apps.foo.models. heh.
            dirpath = find_loader(modulename).path
            if dirpath.endswith("__init__.py"):
                dirpath = os.path.dirname(dirpath)
            path = os.path.join(dirpath, "{}.py".format(extraname))

        with open(path) as rf:
            self.modules[fullname] = self.builder.string_build(rf.read())
        return self.modules[fullname]

    def get_symbol(self, modname, name):
        try:
            module = self.get_module(modname)
        except FindModuleError:
            module = self.get_module(*modname.rsplit(".", 1))
        return module[name]


mcache = FromStmtImportedCache()


def is_toplevel_module(module):
    return module.parent is None


def getattribute(target, gattr):
    while isinstance(gattr, Getattr):
        target = target[gattr.attrname]
        gattr = gattr.expr
    return target


def trasform_from(from_stmt):
    module = from_stmt.parent
    if not is_toplevel_module(module):
        return
    mcache.register_from_stmt(module, from_stmt)


def _get_model_spec_with_oldstyle(cls):
    lhs = cls["FACTORY_FOR"]
    rhs = lhs.parent.value
    try:
        rvalue = list(rhs.infer())[0]  # xxx:
        if isinstance(rvalue, Const):
            # when FACTORY_FOR = "app.models.User"
            modulename, attrname = rvalue.value.rsplit(".", 1)
            return mcache.get_symbol(modulename, attrname)
        return rvalue  # xxx:
    except UnresolvableName as e:
        # when FACTORY_FOR = models.User
        target = mcache.get_symbol_from_stmt(cls.parent, e.args[0])
        return getattribute(target, rhs)


def _get_model_spec_with_newstyle(cls):
    pass


def trasform_class(cls):
    if not is_toplevel_module(cls.parent):
        return
    # this is ad-hock approach. TODO: fix retrieving base class's information.
    if any(name == "DjangoModelFactory" for name in cls.basenames):
        if "FACTORY_FOR" in cls:
            model = _get_model_spec_with_oldstyle(cls)
        elif "Meta" in cls:
            model = _get_model_spec_with_newstyle(cls)
        for name, attr in model.locals.items():
            if name not in cls.locals:
                cls.locals[name] = attr


def register_transform(manager):
    manager.register_transform(scoped_nodes.From, trasform_from)
    manager.register_transform(scoped_nodes.Class, trasform_class)
