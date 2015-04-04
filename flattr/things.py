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
    _fields = {
            'resource': {'read_only': True},
            'link': {'read_only': True},
            'id': {'read_only': True},
            'flattrs': {'read_only': True},
            'flattr_user_count': {'read_only': True},
            'created_at': {'read_only': True},
            'owner': {'read_only': True},
            'flattred': {'read_only': True},
            'last_flattr_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'url': {'validators': isUrl},
            'title': {'validators': isStr},
            'description': {'validators': isStr},
            'tags': {'validators': isStrList},
            'language': {'validators': isStr},
            'category': {'validators': isStr},
            'hidden': {'validator': lambda x: True,
                       'default': False}
            }

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
