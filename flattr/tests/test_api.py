from flattr import api
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
    flattr_api = api.BaseApi(session)

    assert flattr_api._session == session

def test_FlattrApi():
    #with raises(TypeError):
    #    flattr_api = api.FlattrApi('')

    session = requests.Session()
    flattr_api = api.FlattrApi(session)

    assert flattr_api._session == session

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

    with raises(NotImplemented):
        flattr_api.activities
    with raises(NotImplemented):
        flattr_api.languages
    with raises(NotImplemented):
        flattr_api.categories
