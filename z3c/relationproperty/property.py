import types

from .util import obj2rel


_marker = object()


class RelationProperty(object):
    def __init__(self, field, name=None):
        if name is None:
            name = field.__name__

        self.__field = field
        self.__name = name

    def __get__(self, inst, klass):
        if inst is None:
            return self

        value = inst.__dict__.get(self.__name + '_rel', _marker)
        if value is _marker:
            field = self.__field.bind(inst)
            value = getattr(field, 'default', _marker)
            if value is _marker:
                raise AttributeError(self.__name)

        if value is not None:
            vtype = type(value)
            if vtype in (types.ListType, set, tuple):
                # we do not list broken relations (to_object == None)
                value = vtype([v.to_object for v in value
                               if v.to_object is not None])
            else:
                value = value.to_object

        return value

    def __set__(self, inst, value):
        field = self.__field.bind(inst)
        field.validate(value)
        if value is not None:
            vtype = type(value)
            if vtype in (types.ListType, set, tuple):
                value = vtype([obj2rel(v) for v in value])
            else:
                value = obj2rel(value)
        if field.readonly and self.__name in inst.__dict__:
            raise ValueError(self.__name, 'field is readonly')
        inst.__dict__[self.__name + '_rel'] = value

    def __getattr__(self, name):
        return getattr(self.__field, name)
