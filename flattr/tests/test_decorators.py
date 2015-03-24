import six
import types
from pytest import raises
from flattr import result
from flattr.exc import NotFoundError, InvalidScopeError
from simplejson.decoder import JSONDecodeError

class FakeResponse:
    def __init__(self, status_code, error_name):
        self.status_code = status_code
        self.error_name = error_name

    def json(self):
        if self.status_code == 404:
            raise JSONDecodeError('something', 'went wrong', 10)
        elif self.status_code != 200:
            return {'error': self.error_name,
                'error_description': 'something, somewhere, somehow went wrong'}
        return {'some': 'correct json'}

    @property
    def text(self):
        if self.status_code == 404:
            return "404 Not found"

class FakeResponseList(FakeResponse):

    def json(self):
        if self.status_code != 200:
            return {'error': self.error_name,
                'error_description': 'something, somewhere, somehow went wrong'}
        return [{'some': 'correct json'}]


class DummyReturn:
    def __init__(self, *args, **kwargs):
        for k, v in six.iteritems(kwargs):
            setattr(self, k, v)

def test_result_fails():
    with raises(NotFoundError):
        res = result(DummyReturn)(lambda: FakeResponse(404, 'not_found'))()

    with raises(InvalidScopeError):
        result(DummyReturn)(lambda: FakeResponse(403, 'invalid_scope'))()

def test_result():
    res = result(DummyReturn)(lambda: FakeResponse(200, 'nothing'))()

    assert isinstance(res, DummyReturn)
    assert res.some == 'correct json'

def test_result_list():
    gen = result(DummyReturn)(lambda: FakeResponseList(200, 'nothing'))()

    assert isinstance(gen, types.GeneratorType)

    res = next(gen)
    assert isinstance(res, DummyReturn)
    assert res.some == 'correct json'

    with raises(StopIteration):
        next(gen)
