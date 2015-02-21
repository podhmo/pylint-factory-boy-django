# -*- coding:utf-8 -*-
def register_transforms(manager):
    from . import modelfactory
    modelfactory.register_transform(manager)
