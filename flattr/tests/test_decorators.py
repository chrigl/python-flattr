import six
import types
from pytest import raises
import flattr
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

class DummyRequestClass:
    def __init__(self):
        self._session = 'FAKE_SESSION'


class DummyReturn:
    def __init__(self, *args, **kwargs):
        for k, v in six.iteritems(kwargs):
            setattr(self, k, v)

def test_result_fails():
    with raises(NotFoundError):
        res = flattr.result(DummyReturn)(lambda self: FakeResponse(404, 'not_found'))(DummyRequestClass())

    with raises(InvalidScopeError):
        flattr.result(DummyReturn)(lambda self: FakeResponse(403, 'invalid_scope'))(DummyRequestClass())

def test_result():
    res = flattr.result(DummyReturn)(lambda self: FakeResponse(200, 'nothing'))(DummyRequestClass())

    assert isinstance(res, DummyReturn)
    assert res.some == 'correct json'

def test_result_list():
    gen = flattr.result(DummyReturn)(lambda self: FakeResponseList(200, 'nothing'))(DummyRequestClass())

    assert isinstance(gen, types.GeneratorType)

    res = next(gen)
    assert isinstance(res, DummyReturn)
    assert res.some == 'correct json'

    with raises(StopIteration):
        next(gen)

def test_result_None():
    # if the response is None, very likely, the call did not happen, because
    # not necessary in this case. e.g. it is not necessary to update a thing
    # if it is not dirty. So we can save api-calls if nothing real is to do.
    res = flattr.result(DummyReturn)(lambda self: None)(DummyRequestClass())

    assert res == None

def test_api_call():
    def _fake_func(self, a='b'):
        return {'a': a}
    class DummySession:
        def get(self, url, params=None):
            return url, params

    class DummyRequest:
        _session = DummySession()
        _my = 'hello'
        def _get_url(self):
            return 'http://localhost'

    dummy = DummyRequest()
    ret = flattr._api_call('/my/test/foo')(_fake_func)(dummy)
    assert ret == ('http://localhost/my/test/foo', {'a': 'b'})

    ret = flattr._api_call('/:my/test/foo')(_fake_func)(dummy, a='c')
    assert ret == ('http://localhost/hello/test/foo', {'a': 'c'})

    ret = flattr._api_call('/my/')(lambda x: 'test,foo')(dummy)
    assert ret == ('http://localhost/my/test,foo', {})

    ret = flattr._api_call('/my')(lambda x: 'test,foo')(dummy)
    assert ret == ('http://localhost/my/test,foo', {})

    ret = flattr._api_call('/my')(lambda x: False)(dummy)
    assert ret == None

    ret = flattr._api_call('/my/test/foo',
            additional_params={'_method': 'patch'})(_fake_func)(dummy)
    assert ret == ('http://localhost/my/test/foo', {'a': 'b', '_method': 'patch'})

def test_get():
    def _fake_func(self, a='b'):
        return {'a': a}
    class DummySession:
        def get(self, url, params=None):
            return url, params

    class DummyRequest:
        _session = DummySession()
        _my = 'hello'
        def _get_url(self):
            return 'http://localhost'

    dummy = DummyRequest()
    ret = flattr.get('/my/test/foo')(_fake_func)(dummy)
    assert ret == ('http://localhost/my/test/foo', {'a': 'b'})

    ret = flattr.get('/:my/test/foo')(_fake_func)(dummy, a='c')
    assert ret == ('http://localhost/hello/test/foo', {'a': 'c'})

    ret = flattr.get('/my/')(lambda x: 'test,foo')(dummy)
    assert ret == ('http://localhost/my/test,foo', {})

    ret = flattr.get('/my')(lambda x: 'test,foo')(dummy)
    assert ret == ('http://localhost/my/test,foo', {})

def test_post():
    def _fake_func(self, a='b'):
        return {'a': a}
    class DummySession:
        def post(self, url, data=None):
            return url, data

    class DummyRequest:
        _session = DummySession()
        _my = 'hello'
        def _get_url(self):
            return 'http://localhost'

    dummy = DummyRequest()
    ret = flattr.post('/my/test/foo')(_fake_func)(dummy)
    assert ret == ('http://localhost/my/test/foo', {'a': 'b'})

    ret = flattr.post('/:my/test/foo')(_fake_func)(dummy, a='c')
    assert ret == ('http://localhost/hello/test/foo', {'a': 'c'})

    ret = flattr.post('/my/')(lambda x: 'test,foo')(dummy)
    assert ret == ('http://localhost/my/test,foo', {})

    ret = flattr.post('/my')(lambda x: 'test,foo')(dummy)
    assert ret == ('http://localhost/my/test,foo', {})
