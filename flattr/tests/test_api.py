from flattr import api
import flattr.base
import flattr.things
from pytest import raises
import requests

def test_get():
    x = api.get('FAKE_TOKEN')

    assert isinstance(x, api.FlattrApi)
    assert x._session.headers['Authorization'] == 'Bearer FAKE_TOKEN'

    assert x._session.headers['Accept'] == 'application/json'

def test_BaseApi():
    #with raises(TypeError):
    #    flattr_api = api.BaseApi('')

    session = requests.Session()
    flattr_api = flattr.base.BaseApi(session)

    assert flattr_api._session == session

    old_api_url = flattr_api._api_url
    flattr_api._api_url = None
    with raises(AssertionError):
        flattr_api._get_url()

    flattr_api._api_url = old_api_url
    with raises(AssertionError):
        flattr_api._get_url()

    flattr_api._endpoint = 'endpoint'
    res = flattr_api._get_url()
    assert res == 'https://api.flattr.com/endpoint'

    with raises(NotImplementedError):
        flattr_api.new()

def test_FlattrApi_new():
    session = requests.Session()
    flattr_api = api.ThingApi(session)

    assert flattr_api._session == session

    res = flattr_api.new(id=1, title='Hello World')
    assert isinstance(res, flattr.things.Thing)
    assert res._session == session
    assert res.id == 1
    assert res.title == 'Hello World'

def test_FlattrApi():
    session = requests.Session()
    flattr_api = api.FlattrApi(session)

    assert hasattr(flattr_api, 'things')
    assert hasattr(flattr_api, 'users')
    assert hasattr(flattr_api, 'flattrs')
    assert hasattr(flattr_api, 'subscriptions')
    assert hasattr(flattr_api, 'activities')
    assert hasattr(flattr_api, 'categories')
    assert hasattr(flattr_api, 'languages')

    assert flattr_api.things._session == session
    assert flattr_api.users._session == session
    assert flattr_api.flatters._session == session
    assert flattr_api.subscriptions._session == session

    with raises(NotImplementedError):
        flattr_api.activities
    with raises(NotImplementedError):
        flattr_api.languages
    with raises(NotImplementedError):
        flattr_api.categories
