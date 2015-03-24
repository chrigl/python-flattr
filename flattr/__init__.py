from functools import wraps
import requests
from simplejson.decoder import JSONDecodeError
from flattr.exc import raise_exception

def result(cls):
    def _result(fn):
        @wraps(fn)
        def __result(*args, **kwargs):
            resp = fn(*args, **kwargs)
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
                return (cls(**elm) for elm in res)
            else:
                return cls(**res)
        return __result
    return _result
