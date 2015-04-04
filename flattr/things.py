import flattr
import flattr.flattrs
import flattr.resource
from flattr.validators import validate
from flattr.validators import isStr
from flattr.validators import isStrList
from flattr.validators import isUrl
from flattr.validators import isBool

class Thing(flattr.resource.Resource):
    """ flattr able `thing.
    http://developers.flattr.net/api/resources/things/`_ """

    _endpoint = 'rest/v2/things'

    def __init__(self, session=None, resource=None, link=None, id=None,
                 flattrs=None, flattrs_user_count=None, created_at=None,
                 owner=None, image=None, flattred=None, last_flattr_at=None,
                 updated_at=None, title=None, description=None, url=None,
                 tags=None, category=None, language=None, hidden=False,
                 dirty=True):
        """ Initialize with data of an dictionary """
        super(Thing, self).__init__(session)
        # ro fields
        # Do not check any types.
        self._resource = resource
        self._link = link
        self._id = id
        self._flattrs = flattrs
        self._flattrs_user_count = flattrs_user_count
        self._created_at = created_at
        self._owner = owner
        self._image = image
        self._flattred = flattred
        self._last_flattr_at = last_flattr_at
        self._updated_at = updated_at
        # rw fields
        # Checking types. Implicit via validate on fields.
        if title:
            self.title = title
        if description:
            self.description = description
        if url:
            self.url = url
        if tags:
            self.tags = tags
        if language:
            self.language = language
        if category:
            self.category = category
        self.hidden = hidden

        self._dirty = dirty

    # Most of the fields are readonly since you can not modify them on flattr
    @property
    def resource(self):
        """ Returns resource """
        return getattr(self, '_resource', None)

    @property
    def link(self):
        """ Returns link """
        return getattr(self, '_link', None)

    @property
    def id(self):
        """ Returns id """
        return getattr(self, '_id', None)

    @property
    def flattrs(self):
        """ Returns flattrs """
        return getattr(self, '_flattrs', None)

    @property
    def flattrs_user_count(self):
        """ Returns flattrs_user_count """
        return getattr(self, '_flattrs_user_count', None)

    @property
    def created_at(self):
        """ Returns created_at """
        return getattr(self, '_created_at', None)

    @property
    def owner(self):
        """ Returns owner """
        return getattr(self, '_owner', None)

    @property
    def image(self):
        """ Returns image """
        return getattr(self, '_image', None)

    @property
    def flattred(self):
        """ Returns flattred """
        return getattr(self, '_flattred', None)

    @property
    def last_flattr_at(self):
        """ Returns last_flattr_at """
        return getattr(self, '_last_flattr_at', None)

    @property
    def updated_at(self):
        """ Returns updated_at """
        return getattr(self, '_updated_at', None)

    # Some fields are writeable. Only those are submitted to the flattr api.
    @property
    def url(self):
        """ Returns url """
        return getattr(self, '_url', None)

    @url.setter
    @validate(isUrl)
    def url(self, v):
        """ set url """
        self._url = v
        self._dirty = True

    @property
    def title(self):
        """ Returns title """
        return getattr(self, '_title', None)

    @title.setter
    @validate(isStr)
    def title(self, v):
        """ set title """
        self._title = v
        self._dirty = True

    @property
    def description(self):
        """ Returns description """
        return getattr(self, '_description', None)

    @description.setter
    @validate(isStr)
    def description(self, v):
        """ set description """
        self._description = v
        self._dirty = True

    @property
    def tags(self):
        """ Returns tags """
        return getattr(self, '_tags', None)

    @tags.setter
    @validate(isStrList)
    def tags(self, v):
        """ set tags """
        self._tags = v
        self._dirty = True

    @property
    def language(self):
        """ Returns language """
        return getattr(self, '_language', None)

    @language.setter
    @validate(isStr)
    def language(self, v):
        """ set language """
        self._language = v
        self._dirty = True

    @property
    def category(self):
        """ Returns category """
        return getattr(self, '_category', None)

    @category.setter
    @validate(isStr)
    def category(self, v):
        """ set category """
        self._category = v
        self._dirty = True

    @property
    def hidden(self):
        """ Returns hidden """
        return getattr(self, '_hidden', False)

    @hidden.setter
    @validate(isBool)
    def hidden(self, v):
        """ set hidden """
        self._hidden = v
        self._dirty = True

    # we also need some functionality
    def support(self):
        """ Flattr this particular thing.
        Will not work if it's your thing. """
        raise NotImplementedError

    def commit(self):
        """ Create thing, or update if existing. """
        raise NotImplementedError

    def refresh(self):
        """ Refresh this particular thing. Only works if it exists already on
        flattr (id, resource, etc. obtained from flattr) """
        raise NotImplementedError

    @flattr.result(flattr.flattrs.Flattr)
    @flattr.get('/:id/flattrs')
    def get_flattrs(self, count=None, page=None, full=False):
        return flattr._get_query_dict(count=count, page=page, full=full)
