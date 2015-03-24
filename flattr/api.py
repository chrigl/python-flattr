# -*- coding: utf-8 -*-
import requests
from flattr import result

def get(auth_token):
    session = requests.Session()
    session.headers.update({'Accept': 'application/json',
        'Authorization': 'Bearer %s' % auth_token})
    return FlattrApi(session)

class BaseApi:
    def __init__(self, session):
        """Just use session. This is pretty much an abstract class.
        session should be of type requests.sessions.Session."""
        self._session = session

class ThingApi(BaseApi):

    def list_own(self):
        """Returns list of authenticated users things"""
        res = self._session.get('https://api.flattr.com/rest/v2/user/things')


things = ThingApi(None)

class FlattrApi(BaseApi):

    def __init__(self, session):
        """Set the session."""
        super(FlattrApi, self).__init__(session)
        self._things = things
        self._things._session = session
