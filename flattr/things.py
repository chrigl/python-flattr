from flattr.validators import validate
from flattr.validators import isStr
from flattr.validators import isStrList
from flattr.validators import isUrl
from flattr.validators import isBool

class Thing(object):
    """ flattr able `thing.
    http://developers.flattr.net/api/resources/things/`_ """

    def __init__(self, **kw):
        """ Initialize with data of an dictionary """
        
        # ro fields
        # Do not check any types.
        if 'resource' in kw:
            self._resource = kw['resource']
        if 'link' in kw:
            self._link = kw['link']
        if 'id' in kw:
            self._id = kw['id']
        if 'flattrs' in kw:
            self._flattrs = kw['flattrs']
        if 'flattrs_user_count' in kw:
            self._flattrs_user_count = kw['flattrs_user_count']
        if 'created_at' in kw:
            self._created_at = kw['created_at']
        if 'owner' in kw:
            self._owner = kw['owner']
        if 'image' in kw:
            self._image = kw['image']
        if 'flattred' in kw:
            self._flattred = kw['flattred']
        if 'last_flattr_at' in kw:
            self._last_flattr_at = kw['last_flattr_at']
        if 'updated_at' in kw:
            self._updated_at = kw['updated_at']
        # rw fields
        # Checking types. Implicit via validate on fields.
        if 'title' in kw:
            self.title = kw['title']
        if 'description' in kw:
            self.description = kw['description']
        if 'url' in kw:
            self.url = kw['url']
        if 'tags' in kw:
            self.tags = kw['tags']
        if 'language' in kw:
            self.language = kw['language']
        if 'category' in kw:
            self.category = kw['category']
        if 'hidden' in kw:
            self.hidden = kw['hidden']
        else:
            self._hidden = False

        # by default this object is dirty, because I assume it is
        # created as a new object. The api is aware of setting it
        # to False
        if 'dirty' in kw:
            self._dirty = kw['dirty']
        else:
            self._dirty = True

    # Most of the fields are readonly since you can not modify them on flattr
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
    def id(self):
        """ Returns id """
        if not hasattr(self, '_id'):
            return None
        return self._id

    @property
    def flattrs(self):
        """ Returns flattrs """
        if not hasattr(self, '_flattrs'):
            return None
        return self._flattrs

    @property
    def flattrs_user_count(self):
        """ Returns flattrs_user_count """
        if not hasattr(self, '_flattrs_user_count'):
            return None
        return self._flattrs_user_count

    @property
    def created_at(self):
        """ Returns created_at """
        if not hasattr(self, '_created_at'):
            return None
        return self._created_at

    @property
    def owner(self):
        """ Returns owner """
        if not hasattr(self, '_owner'):
            return None
        return self._owner

    @property
    def image(self):
        """ Returns image """
        if not hasattr(self, '_image'):
            return None
        return self._image

    @property
    def flattred(self):
        """ Returns flattred """
        if not hasattr(self, '_flattred'):
            return None
        return self._flattred

    @property
    def last_flattr_at(self):
        """ Returns last_flattr_at """
        if not hasattr(self, '_last_flattr_at'):
            return None
        return self._last_flattr_at

    @property
    def updated_at(self):
        """ Returns updated_at """
        if not hasattr(self, '_updated_at'):
            return None
        return self._updated_at

    # Some fields are writeable. Only those are submitted to the flattr api.
    @property
    def url(self):
        """ Returns url """
        if not hasattr(self, '_url'):
            return None
        return self._url

    @url.setter
    @validate(isUrl)
    def url(self, v):
        """ set url """
        self._url = v
        self._dirty = True

    @property
    def title(self):
        """ Returns title """
        if not hasattr(self, '_title'):
            return None
        return self._title

    @title.setter
    @validate(isStr)
    def title(self, v):
        """ set title """
        self._title = v
        self._dirty = True

    @property
    def description(self):
        """ Returns description """
        if not hasattr(self, '_description'):
            return None
        return self._description

    @description.setter
    @validate(isStr)
    def description(self, v):
        """ set description """
        self._description = v
        self._dirty = True

    @property
    def tags(self):
        """ Returns tags """
        if not hasattr(self, '_tags'):
            return None
        return self._tags

    @tags.setter
    @validate(isStrList)
    def tags(self, v):
        """ set tags """
        self._tags = v
        self._dirty = True

    @property
    def language(self):
        """ Returns language """
        if not hasattr(self, '_language'):
            return None
        return self._language

    @language.setter
    @validate(isStr)
    def language(self, v):
        """ set language """
        self._language = v
        self._dirty = True

    @property
    def category(self):
        """ Returns category """
        if not hasattr(self, '_category'):
            return None
        return self._category

    @category.setter
    @validate(isStr)
    def category(self, v):
        """ set category """
        self._category = v
        self._dirty = True

    @property
    def hidden(self):
        """ Returns hidden """
        if not hasattr(self, '_hidden'):
            return None
        return self._hidden

    @hidden.setter
    @validate(isBool)
    def hidden(self, v):
        """ set hidden """
        self._hidden = v
        self._dirty = True

    # we also need some functionality
    def flattr(self):
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
