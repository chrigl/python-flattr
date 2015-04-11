# -*- coding: utf-8 -*-
import six
import requests
import flattr
import flattr.user
import flattr.things
import flattr.flattrs
import flattr.subscriptions
import flattr.base
import flattr.search

def get(auth_token):
    session = requests.Session()
    session.headers.update({'Accept': 'application/json',
        'Authorization': 'Bearer %s' % auth_token})
    return FlattrApi(session)

class ThingApi(flattr.base.BaseApi):

    _endpoint = 'rest/v2/things'

    def new(self, *args, **kwargs):
        """Returns new `flattr.things.Thing`, connected to the session.
        For parameters have a look at `flattr.things.Thing`."""
        return flattr.things.Thing(session=self._session, **kwargs)

    @flattr.result(flattr.things.Thing)
    @flattr.get('/')
    def get(self, *args):
        """Get one or more thing.
        Pass as much thing ids as parameter as you need to.
        Returns either one thing, or a generator of things."""
        return ','.join(args)

    @flattr.result(flattr.things.Thing)
    @flattr.get('/lookup')
    def lookup(self, url):
        """Check if a thing exists.
        Returns one thing."""
        return {'url': url}

    @flattr.result(flattr.search.SearchResult)
    @flattr.get('/search')
    def search(self, query=None, url=None, tags=None, language=None,
        category=None, user=None, sort=None, page=None, count=None, full=False):
        """Search a thing

        query (Optional) - string Free text search string
        url (Optional) - string Filter by url
        tags (Optional) - string Filter by tags, see syntax below
        language (Optional) - string Filter by language. If you wan't to search more than one language you can separate them with a , (comma).
        category (Optional) - string Filter by category. If you wan't to search more than one category you can separate them with a , (comma).
        user (Optional) - string Filter by username
        sort (Optional) - string Sort by trend, flattrs (all time), flattrs_month, flattrs_week, flattrs_day or relevance (default)
        page (Optional) - integer The result page to show
        count (Optional) - integer Number of items per page
        full ( Optional ) - Receive full user object instead of small
        """
        q = flattr._get_query_dict(query=query, url=url, tags=tags,
                language=language, category=category, user=user, sort=sort,
                page=page, count=count, full=full)
        return q

class UsersApi(flattr.base.BaseApi):

    _endpoint = 'rest/v2/users'

    def __call__(self, username):
        """Returns user object, only containing username.
        No api-call happens here"""
        return flattr.user.User(session=self._session, username=username)

    @flattr.result(flattr.user.User)
    @flattr.get('/')
    def get(self, username):
        """Get the flattr user."""
        return username

class AuthenticatedApi(flattr.base.BaseApi):

    _endpoint = 'rest/v2/user'

    @flattr.result(flattr.flattrs.Flattr)
    @flattr.get('/flattrs')
    def get_flattrs(self, count=None, page=None, full=None):
        """ Get all flattrs all flattrs, the authenticated user did so far.
        http://developers.flattr.net/api/resources/flattrs/#list-the-authenticated-users-flattrs
        """
        return flattr._get_query_dict(count=count, page=page, full=full)

    @flattr.result(flattr.things.Thing)
    @flattr.get('/things')
    def get_things(self, count=None, page=None, full=None):
        """ Get all things of the authenticated user.
        http://developers.flattr.net/api/resources/things/#list-a-authenticated-users-things
        """
        return flattr._get_query_dict(count=count, page=page, full=full)

    @flattr.result(flattr.subscriptions.Subscription)
    @flattr.get('/subscriptions')
    def get_subscriptions(self):
        """ Get all subscriptions of the authenticated user.
        http://developers.flattr.net/api/resources/subscriptions/#list-subscriptions
        """
        return {}

    @flattr.just_json
    @flattr.get('/activities',
            additional_headers={'Accept': 'application/stream+json'})
    def get_activities(self, type=None):
        """ Get all activities os the authenticated user.
        http://developers.flattr.net/api/resources/activities/#list-a-authenticated-users-activities
        """
        return flattr._get_query_dict(type=type)

things = ThingApi(None)
users = UsersApi(None)
authenticated = AuthenticatedApi(None)

class FlattrApi(flattr.base.BaseApi):

    def __init__(self, session):
        """Set the session."""
        super(FlattrApi, self).__init__(session)
        self.things = things
        self.things._session = session
        self.users = users
        self.users._session = session
        self.authenticated = authenticated
        self.authenticated._session = session
