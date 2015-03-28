# -*- coding: utf-8 -*-

class BaseApi:
    def __init__(self, session):
        """Just use session. This is pretty much an abstract class.
        session should be of type requests.sessions.Session."""
        self._session = session
        self._api_url = 'https://api.flattr.com'

    def _get_url(self):
        assert self._api_url != None
        assert hasattr(self, '_endpoint')
        return '%s/%s' % (self._api_url, self._endpoint)
