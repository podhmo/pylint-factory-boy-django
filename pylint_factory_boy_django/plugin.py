# -*- coding:utf-8 -*-
from . import transforms
from astroid import MANAGER


def register(linter, manager=MANAGER):
    transforms.register_transforms(manager)
