import flattr
import flattr.things
import flattr.resource
import flattr.flattrs

class User(flattr.resource.Resource):
    """ Flattr users.
    http://developers.flattr.net/api/resources/users/`_ """

    _endpoint = 'rest/v2/users'

    def __init__(self, **kw):
        super(User, self).__init__(session=kw.get('session', None))
        if 'resource' in kw:
            self._resource=kw['resource']
        if 'link' in kw:
            self._link=kw['link']
        if 'username' in kw:
            self._username=kw['username']
        if 'url' in kw:
            self._url=kw['url']
        if 'firstname' in kw:
            self._firstname=kw['firstname']
        if 'lastname' in kw:
            self._lastname=kw['lastname']
        if 'avatar' in kw:
            self._avatar=kw['avatar']
        if 'about' in kw:
            self._about=kw['about']
        if 'city' in kw:
            self._city=kw['city']
        if 'country' in kw:
            self._country=kw['country']
        if 'email' in kw:
            self._email=kw['email']
        if 'registered_at' in kw:
            self._registered_at=kw['registered_at']

    @property
    def resource(self):
        """ Returns resource """
        if not hasattr(self, '_resource'):
            return None
        return self._resource

    @property
    def link(self):
        """ Returns link """
        if not hasattr(self, '_link'):
            return None
        return self._link

    @property
    def username(self):
        """ Returns username """
        if not hasattr(self, '_username'):
            return None
        return self._username

    @property
    def url(self):
        """ Returns url """
        if not hasattr(self, '_url'):
            return None
        return self._url

    @property
    def firstname(self):
        """ Returns firstname """
        if not hasattr(self, '_firstname'):
            return None
        return self._firstname

    @property
    def lastname(self):
        """ Returns lastname """
        if not hasattr(self, '_lastname'):
            return None
        return self._lastname

    @property
    def avatar(self):
        """ Returns avatar """
        if not hasattr(self, '_avatar'):
            return None
        return self._avatar

    @property
    def about(self):
        """ Returns about """
        if not hasattr(self, '_about'):
            return None
        return self._about

    @property
    def city(self):
        """ Returns city """
        if not hasattr(self, '_city'):
            return None
        return self._city

    @property
    def country(self):
        """ Returns country """
        if not hasattr(self, '_country'):
            return None
        return self._country

    @property
    def email(self):
        """ Returns email """
        if not hasattr(self, '_email'):
            return None
        return self._email

    @property
    def registered_at(self):
        """ Returns registered_at """
        if not hasattr(self, '_registered_at'):
            return None
        return self._registered_at

    @flattr.result(flattr.things.Thing)
    @flattr.get('/:username/things')
    def get_things(self, count=None, page=None, full=False):
        return flattr._get_query_dict(count=count, page=page, full=full)

    @flattr.result(flattr.flattrs.Flattr)
    @flattr.get('/:username/flattrs')
    def get_flattrs(self, count=None, page=None, full=False):
        return flattr._get_query_dict(count=count, page=page, full=full)
