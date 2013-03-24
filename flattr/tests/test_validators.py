from flattr.validators import isInt
from flattr.validators import isBool
from flattr.validators import isStr
from flattr.validators import isBinary
from flattr.validators import isFloat
from flattr.validators import isUrl
from flattr.validators import validate
import sys
from pytest import raises

def test_isStr():
    if sys.version < '3':
        assert isStr(u'Hällö') == True
        assert isStr('Hällö') == False
    else:
        assert isStr('Hällö') == True

def test_isBinary():
    if sys.version < '3':
        assert isBinary('Hello') == True
    else:
        assert isBinary('Hello') == False

def test_isUrl():
    if sys.version < '3':
        assert isUrl('hello') == False
        assert isUrl('http://a') == False
        assert isUrl('https://b') == False

        assert isUrl(u'hello') == False
        assert isUrl(u'http://a') == True
        assert isUrl(u'https://b') == True
    else:
        assert isUrl(b'hello') == False
        assert isUrl(b'http://a') == False
        assert isUrl(b'https://b') == False

        assert isUrl('hello') == False
        assert isUrl('http://a') == True
        assert isUrl('https://b') == True

def test_validate():
    @validate(isInt)
    def foo(x):
        return x

    assert foo(1) == 1

    with raises(TypeError):
        foo('Hello')

    with raises(TypeError):
        foo(1, 2)

def test_validate_cls():
    class A(object):
        @validate(isInt)
        def foo(self, x):
            return x

    a = A()

    assert a.foo(1) == 1

    with raises(TypeError):
        a.foo('Hello')

    with raises(TypeError):
        a.foo(1, 2)

    try:
        a.foo(1, 2)
    except TypeError as e:
        assert str(e) == 'foo() takes 2 positional arguments but 3 were given'
    

def test_validate_with_property():
    class A(object):
        def __init__(self):
            self._x = 0

        @property
        def x(self):
            return self._x

        @x.setter
        @validate(isInt)
        def x(self, v):
            self._x = v

    a = A()

    assert a.x == 0
    assert a._x == 0

    a.x = 1
    assert a.x == 1
    assert a._x == 1

    with raises(TypeError):
        a.x = 'Hello'

    with raises(TypeError):
        a.x = 1, 2

    try:
        a.x = 1, 2
    except TypeError as e:
        assert str(e) == '(1, 2) does not match isInt'
