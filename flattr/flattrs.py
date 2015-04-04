import flattr.resource

class Flattr(flattr.resource.Resource):
    def __init__(self, session=None, thing=None, owner=None, created_at=None):
        """A flattr/support object"""
        self._thing = thing
        self._owner = owner
        self._created_at = created_at

    @property
    def thing(self):
        """ Returns thing """
        return getattr(self, '_thing', None)

    @property
    def owner(self):
        """ Returns owner """
        return getattr(self, '_owner', None)

    @property
    def created_at(self):
        """ Returns created_at """
        return getattr(self, '_created_at', None)
