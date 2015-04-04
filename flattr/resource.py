# -*- coding: utf-8 -*-
import six
import flattr.base
import flattr.validators

# inserting some black magick
def silly_getter(field):
    fieldname = '_%s' % field
    def _silly_getter(self):
        if not hasattr(self, fieldname):
            return None
        return getattr(self, fieldname)
    return _silly_getter

def silly_setter(field):
    fieldname = '_%s' % field
    def _silly_setter(self, v):
        setattr(self, fieldname, v)
    return _silly_setter

class MetaResource(type):
    """So... what the heck are you doing?

    This stuff enables you to define fields in resources by using the
    the class param _fields. Each field consits of the field name and a
    validator (see flattr.validators). If you do not need a validator,
    use lambda x: True.

    e.g.:
    _fields = {'field1': flattr.validators.isInt,
               'field2': flattr.validators.isUrl,
               'field3': lambda x: True}

    What happens under the hoot?
    A property named 'field1' will be created, as well as the corresponding
    setter. You can set values with:
        ob.field1 = 1

    or get it back via:
        ret = ob.field1

    Without _fields you have do define each field yourself:

        @property
        def field1(self):
            return getattr(self, '_field1', None)

        @field1.setter
        @validate(isInt)
        def field1(self, v):
            self._field1 = v
    """
    def __init__(cls, name, bases, dct):
        if hasattr(cls, '_fields'):
            for field, settings in six.iteritems(cls._fields):
                field_validators = settings.get('validators', [lambda x: True])
                read_only = settings.get('read_only', False)
                try:
                    validators = iter(field_validators)
                except TypeError:
                    validators = [field_validators]
                setattr(cls, field, property(silly_getter(field)))
                if not read_only:
                    real_field = getattr(cls, field)
                    fn = silly_setter(field)
                    for validator in validators:
                        fn = flattr.validators.validate(validator)(fn)
                    setattr(cls, field, real_field.setter(fn))
        return super(MetaResource, cls).__init__(name, bases, dct)

@six.add_metaclass(MetaResource)
class Resource(flattr.base.BaseApi):
    def __init__(self, **kw):
        super(Resource, self).__init__(kw.get('session', None))
        if hasattr(self, '_fields'):
            for field, settings in six.iteritems(self._fields):
                default = settings.get('default', None)
                try:
                    setattr(self, '_%s' % field, kw.get(field, default))
                except AttributeError:
                    raise AttributeError("Can't set attribute %s" % field)
