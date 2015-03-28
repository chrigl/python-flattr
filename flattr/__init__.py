import re
import six
import functools
import requests
from simplejson.decoder import JSONDecodeError
from flattr.exc import raise_exception

def result(cls):
    def _result(fn):
        @functools.wraps(fn)
        def __result(self, *args, **kwargs):
            resp = fn(self, *args, **kwargs)
            if resp.status_code != 200:
                try:
                    res = resp.json()
                    error = res['error']
                    description = res['error_description']
                except JSONDecodeError:
                    # just a hack, since 404 could come without json-body
                    error = 'not_found'
                    description = resp.text
                raise_exception(resp.status_code, error, description)
            res = resp.json()
            if isinstance(res, list):
                return (cls(session=self._session, **elm) for elm in res)
            else:
                return cls(session=self._session, **res)
        return __result
    return _result

def _replace_(ob, parts):
    """Repaces parts by object values
    >>> class A:
    ...     _username = 'my'
    ...     _testing = 'test'
    >>> '/'.join(_replace_(A(), ['this', ':username', 'is', ':testing', 'stuff']))
    'this/my/is/test/stuff'
    """
    for part in parts:
        if part.startswith(':'):
            yield str(getattr(ob, '_%s' % part[1:]))
        else:
            yield part

def get(map_url):
    def _get(fn):
        @functools.wraps(fn)
        def __get(self, *args, **kwargs):
            params = fn(self, *args, **kwargs)
            if ':' in map_url:
                _map_url = '/'.join(_replace_(self, map_url.split('/')))
            else:
                _map_url = map_url
            url = '%s%s' % (self._get_url(), _map_url)
            q = {}
            if isinstance(params, six.string_types):
                if url.endswith('/'):
                    url += params
                else:
                    url += '/' + params
            else:
                q = params
            return self._session.get(url, params=q)
        return __get
    return _get

def _get_query_dict(**kwargs):
    """Returns query dict by kwargs.
    Skip None-values, but keeps False etc.
    >>> res = _get_query_dict(url=None, test='a', page=True, full=False)
    >>> res == {'test': 'a', 'page': True, 'full': False}
    True
    """
    def __get_quey_dict(**kwargs):
        for k, v in six.iteritems(kwargs):
            if v is not None:
                yield k, v
    return dict(__get_quey_dict(**kwargs))
