
class Flattrs:
    def __init__(self, **kw):

        if 'thing' in kw:
            self._thing = kw['thing']
        if 'owner' in kw:
            self._owner = kw['owner']
        if 'created_at' in kw:
            self._created_at = kw['created_at']

    @property
    def thing(self):
        """ Returns thing """
        if not hasattr(self, '_thing'):
            return None
        return self._thing

    @property
    def owner(self):
        """ Returns owner """
        if not hasattr(self, '_owner'):
            return None
        return self._owner

    @property
    def created_at(self):
        """ Returns created_at """
        if not hasattr(self, '_created_at'):
            return None
        return self._created_at
