# -*- coding: utf-8 -*-
import requests

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

class FlattrApi(BaseApi):
    pass
