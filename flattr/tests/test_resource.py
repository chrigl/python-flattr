from flattr.resource import Resource

def test_resource():
    r = Resource(None)

    res = repr(r)

    assert res == '<flattr.resource.Resource at %s>' % id(r)
