from __future__ import absolute_import


class MenuLessObject(object):
    """
    A simple class to hold the list of object for which a top menu
    navigation will be supressed
    """
    _objects = []

    @classmethod
    def get_all_objects(cls):
        return tuple(cls._objects)

    def __init__(self, obj):
        self.obj = obj
        self.__class__._objects.append(obj)
