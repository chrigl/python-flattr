from __future__ import unicode_literals
import sys
import re
import itertools

url_pat = re.compile('^https?://')

def isInt(x):
    """ Returns True, if x is an integer.
    >>> isInt(1)
    True
    >>> isInt('Hello')
    False
    >>> isInt(3.14)
    False
    """
    return isinstance(x, int)

def isFloat(x):
    """ Returns True, if x is an float.
    >>> isFloat(3)
    False
    >>> isFloat(3.14)
    True
    >>> isFloat('3.14')
    False
    """
    return isinstance(x, float)

def isBool(x):
    """ Returns True, if x is a boolean.
    >>> isBool(True)
    True
    >>> isBool(False)
    True
    >>> isBool(1)
    False
    >>> isBool(0)
    False
    """
    return isinstance(x, bool)

def isStr(x):
    """ Returns True, if x is a string.
    Knows about the difference between python2 and 3.
    >>> isStr(b'Hello')
    False
    >>> isStr(5)
    False

    There are more python version dependend tests in
    tests/test_validators.py
    """
    if sys.version < '3':
        return isinstance(x, unicode)
    return isinstance(x, str)

def isBinary(x):
    """ Returns True, if x is a binary.
    Knows about the difference between python2 and 3.
    >>> isBinary(b'Hello')
    True

    There are more python version dependend tests in
    tests/test_validators.py
    """
    if sys.version < '3':
        return isinstance(x, str)
    return isinstance(x, bytes)

def isUrl(x):
    """ Returns True, if x is an url """
    if not isStr(x):
        return False
    return url_pat.match(x) != None

def validate(validator):
    """ Decorator to use a specified validator for your function/method. """
    def _validate(fn):
        def __validate(*p):
            # take an array of parameters, because in classes we get self, x.
            # In functions just x
            if len(p) > fn.__code__.co_argcount:
                raise TypeError('%s() takes %s positional arguments but %s were given' % (fn.__name__, fn.__code__.co_argcount, len(p)))
            if not validator(p[-1]):
                raise TypeError('%s does not match %s' % (p[-1], validator.__name__))
            return fn(*p)
        return __validate
    return _validate
