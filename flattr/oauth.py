import flattr
import flattr.base
import requests
from requests.auth import HTTPBasicAuth

def get():
    return AuthApi(requests.Session())

class AuthApi(flattr.base.BaseApi):

    _endpoint = 'oauth'

    def __init__(self, session):
        super(AuthApi, self).__init__(session)
        self._api_url = 'https://flattr.com'

    def set_auth(self, client_id, client_secret):
        """ Set credentials to get a token. """
        self._session.auth = HTTPBasicAuth(client_id, client_secret)

    def authorize(self, client_id, scope, redirect_uri, response_type='code'):
        """ Returns url. You have to send the user to this url.
        There, the user will, or will not authorize the app.
        Then he/she will be returned to redirect_uri. Either with code as param,
        or a json with an error message. Depending on the choice.
        http://developers.flattr.net/api/#authorization
        """
        req = requests.Request('GET', '%s/%s/authorize' %
                (self._api_url, self._endpoint),
            params={'client_id': client_id,
                    'scope': scope,
                    'redirect_uri': redirect_uri,
                    'response_type': response_type})
        prep_req = req.prepare()
        return prep_req.url

    @flattr.just_json
    @flattr.post('/token')
    def token(self, code, redirect_uri, grant_type='authorization_code'):
        """ Returns the access token, you should use with flattr.api.get.
        """
        return {'code': code,
                'redirect_uri': redirect_uri,
                'grant_type': grant_type}
