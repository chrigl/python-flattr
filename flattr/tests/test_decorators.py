import six
import types
import pytest
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

@pytest.fixture
def fake_response_cls():
    return FakeResponse

@pytest.fixture
def fake_response_list_cls():
    return FakeResponseList

@pytest.fixture
def dummy_request_cls():
    return DummyRequestClass

@pytest.fixture
def dummy_return_cls():
    return DummyReturn

def test_result_fails(dummy_return_cls, fake_response_cls, dummy_request_cls):
    with pytest.raises(NotFoundError):
        res = flattr.result(dummy_return_cls)(lambda self: fake_response_cls(404, 'not_found'))(dummy_request_cls())

    with pytest.raises(InvalidScopeError):
        flattr.result(dummy_return_cls)(lambda self: fake_response_cls(403, 'invalid_scope'))(dummy_request_cls())

def test_result(dummy_return_cls, fake_response_cls, dummy_request_cls):
    res = flattr.result(dummy_return_cls)(lambda self: fake_response_cls(200, 'nothing'))(dummy_request_cls())

    assert isinstance(res, dummy_return_cls)
    assert res.some == 'correct json'

def test_result_list(dummy_return_cls, fake_response_list_cls, dummy_request_cls):
    gen = flattr.result(dummy_return_cls)(lambda self: fake_response_list_cls(200, 'nothing'))(dummy_request_cls())

    assert isinstance(gen, types.GeneratorType)

    res = next(gen)
    assert isinstance(res, dummy_return_cls)
    assert res.some == 'correct json'

    with pytest.raises(StopIteration):
        next(gen)

def test_result_None(dummy_return_cls, dummy_request_cls):
    # if the response is None, very likely, the call did not happen, because
    # not necessary in this case. e.g. it is not necessary to update a thing
    # if it is not dirty. So we can save api-calls if nothing real is to do.
    res = flattr.result(dummy_return_cls)(lambda self: None)(dummy_request_cls())

    assert res == None

def test_api_call():
    def _fake_func(self, a='b'):
        return {'a': a}
    class DummySession:
        def __init__(self):
            self.headers = {'Accept': 'application/json', 'One': 'Field'}
        def get(self, url, params=None, headers=None):
            return url, params, headers

    class DummyRequest:
        _session = DummySession()
        _my = 'hello'
        def _get_url(self):
            return 'http://localhost'

    dummy = DummyRequest()
    ret = flattr._api_call('/my/test/foo')(_fake_func)(dummy)
    assert ret == ('http://localhost/my/test/foo', {'a': 'b'}, None)

    ret = flattr._api_call('/:my/test/foo')(_fake_func)(dummy, a='c')
    assert ret == ('http://localhost/hello/test/foo', {'a': 'c'}, None)

    ret = flattr._api_call('/my/')(lambda x: 'test,foo')(dummy)
    assert ret == ('http://localhost/my/test,foo', {}, None)

    ret = flattr._api_call('/my')(lambda x: 'test,foo')(dummy)
    assert ret == ('http://localhost/my/test,foo', {}, None)

    ret = flattr._api_call('/my')(lambda x: False)(dummy)
    assert ret == None

    ret = flattr._api_call('/my/test/foo',
            additional_params={'_method': 'patch'})(_fake_func)(dummy)
    assert ret == ('http://localhost/my/test/foo', {'a': 'b', '_method': 'patch'}, None)

    ret = flattr._api_call('/my/test/foo', additional_headers={'Accept': 'application/stream+json'})(_fake_func)(dummy)
    assert ret == ('http://localhost/my/test/foo', {'a': 'b'},
            {'Accept': 'application/stream+json', 'One': 'Field'})

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
