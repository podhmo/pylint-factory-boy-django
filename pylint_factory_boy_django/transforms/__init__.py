# -*- coding:utf-8 -*-
from astroid import MANAGER
from astroid.builder import AstroidBuilder
from astroid.exceptions import UnresolvableName
from astroid.node_classes import Getattr
# from astroid.as_string import to_code
from astroid import scoped_nodes
from weakref import WeakKeyDictionary, WeakValueDictionary
from importlib import find_loader


class FromStmtImportedCache(object):
    def __init__(self, builder=None):
        self.from_stmt_cache = WeakKeyDictionary()
        self.modules = WeakValueDictionary()
        self.builder = builder or AstroidBuilder(MANAGER)

    def register_from_stmt(self, module, from_stmt):
        self.from_stmt_cache.setdefault(module, []).append(from_stmt)

    def get_imported_attribute(self, parent, target_name):
        for stmt in self.from_stmt_cache[parent]:
            for name, bound in stmt.names:
                if target_name == name:
                    module = self.get_module(stmt.modname)
                    try:
                        return module[name]  # member of module
                    except KeyError:
                        return self.get_module(".".join([stmt.modname, name]))

    def get_module(self, modulename):
        if modulename in self.modules:
            return self.modules[modulename]

        path = find_loader(modulename).path
        with open(path) as rf:
            self.modules[modulename] = self.builder.string_build(rf.read())
            return self.modules[modulename]

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


def trasform_class(cls):
    if cls.name == "Test" and is_toplevel_module(cls.parent):
        lhs = cls["patch"]
        rhs = lhs.parent.value
        try:
            target = list(rhs.infer())[0]  # xxx:
        except UnresolvableName as e:
            target = mcache.get_imported_attribute(cls.parent, e.args[0])
        cls.locals[lhs.name] = [getattribute(target, rhs)]
        print(cls.locals)


def register_transform(manager):
    manager.register_transform(scoped_nodes.From, trasform_from)
    manager.register_transform(scoped_nodes.Class, trasform_class)
