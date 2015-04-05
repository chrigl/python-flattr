import flattr
import flattr.things
import flattr.resource
import flattr.flattrs

class User(flattr.resource.Resource):
    """ Flattr users.
    http://developers.flattr.net/api/resources/users/`_ """

    _endpoint = 'rest/v2/users'

    def __init__(self, session=None, resource=None, link=None,
                 username=None, url=None, firstname=None, lastname=None,
                 avatar=None, about=None, city=None, country=None, email=None,
                 registered_at=None, **kwargs):
        # ignored fields: kwargs
        # so lib will not break if flattr-api adds a new field
        super(User, self).__init__(session)
        self._resource=resource
        self._link=link
        self._username=username
        self._url=url
        self._firstname=firstname
        self._lastname=lastname
        self._avatar=avatar
        self._about=about
        self._city=city
        self._country=country
        self._email=email
        self._registered_at=registered_at

    def __repr_helper__(self):
        return '%s' % self._username

    @property
    def resource(self):
        """ Returns resource """
        return getattr(self, '_resource', None)

    @property
    def link(self):
        """ Returns link """
        return getattr(self, '_link', None)

    @property
    def username(self):
        """ Returns username """
        return getattr(self, '_username', None)

    @property
    def url(self):
        """ Returns url """
        return getattr(self, '_url', None)

    @property
    def firstname(self):
        """ Returns firstname """
        return getattr(self, '_firstname', None)

    @property
    def lastname(self):
        """ Returns lastname """
        return getattr(self, '_lastname', None)

    @property
    def avatar(self):
        """ Returns avatar """
        return getattr(self, '_avatar', None)

    @property
    def about(self):
        """ Returns about """
        return getattr(self, '_about', None)

    @property
    def city(self):
        """ Returns city """
        return getattr(self, '_city', None)

    @property
    def country(self):
        """ Returns country """
        return getattr(self, '_country', None)

    @property
    def email(self):
        """ Returns email """
        return getattr(self, '_email', None)

    @property
    def registered_at(self):
        """ Returns registered_at """
        return getattr(self, '_registered_at', None)

    @flattr.result(flattr.things.Thing)
    @flattr.get('/:username/things')
    def get_things(self, count=None, page=None, full=False):
        return flattr._get_query_dict(count=count, page=page, full=full)

    @flattr.result(flattr.flattrs.Flattr)
    @flattr.get('/:username/flattrs')
    def get_flattrs(self, count=None, page=None, full=False):
        return flattr._get_query_dict(count=count, page=page, full=full)

    def subscribe(self):
        """ Subscribe to this user, if currently unsubscribed. """
        raise NotImplementedError

    def unsubscribe(self):
        """ Unsubscribe from user, if currently subscribed. """
        raise NotImplementedError

