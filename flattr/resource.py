# -*- coding: utf-8 -*-
import flattr.base

class Resource(flattr.base.BaseApi):
    def __repr_helper__(self):
        return 'at %s' % id(self)

    def __repr__(self):
        return '<%s.%s %s>' % (self.__class__.__module__,
                               self.__class__.__name__,
                               self.__repr_helper__())
