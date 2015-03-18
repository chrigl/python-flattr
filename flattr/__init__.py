from functools import wraps
import requests

def map_type(cls):
    def _map_type(fn):
        @wraps(fn)
        def __map_type(*args, **kwargs):
            resp = fn(*args, **kwargs)
            if resp.status_code != 200:
                return None
            res = resp.json()
            if isinstance(res, list):
                return (cls(**elm) for elm in res)
            else:
                return cls(**res)
        return __map_type
    return _map_type
