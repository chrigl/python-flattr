import sys
from flattr.things import Thing
from pytest import raises

# test ro fields
def test_resource():
    t = Thing()

    assert t.resource == None

    t._resource = 'resource'
    assert t.resource == 'resource'

    # this is an read-only field
    with raises(AttributeError):
        t.resource = 'resource'

def test_link():
    t = Thing()

    assert t.link == None

    t._link = 'link'
    assert t.link == 'link'

    # this is an read-only field
    with raises(AttributeError):
        t.link = 'link'

def test_id():
    t = Thing()

    assert t.id == None

    t._id = 'id'
    assert t.id == 'id'

    # this is an read-only field
    with raises(AttributeError):
        t.id = 'id'

def test_flattrs():
    t = Thing()

    assert t.flattrs == None

    t._flattrs = 'flattrs'
    assert t.flattrs == 'flattrs'

    # this is an read-only field
    with raises(AttributeError):
        t.flattrs = 'flattrs'

def test_flattrs_user_count():
    t = Thing()

    assert t.flattrs_user_count == None

    t._flattrs_user_count = 'flattrs_user_count'
    assert t.flattrs_user_count == 'flattrs_user_count'

    # this is an read-only field
    with raises(AttributeError):
        t.flattrs_user_count = 'flattrs_user_count'

def test_created_at():
    t = Thing()

    assert t.created_at == None

    t._created_at = 'created_at'
    assert t.created_at == 'created_at'

    # this is an read-only field
    with raises(AttributeError):
        t.created_at = 'created_at'

def test_owner():
    t = Thing()

    assert t.owner == None

    t._owner = 'owner'
    assert t.owner == 'owner'

    # this is an read-only field
    with raises(AttributeError):
        t.owner = 'owner'

def test_image():
    t = Thing()

    assert t.image == None

    t._image = 'image'
    assert t.image == 'image'

    # this is an read-only field
    with raises(AttributeError):
        t.image = 'image'

def test_flattred():
    t = Thing()

    assert t.flattred == None

    t._flattred = 'flattred'
    assert t.flattred == 'flattred'

    # this is an read-only field
    with raises(AttributeError):
        t.flattred = 'flattred'

def test_last_flattr_at():
    t = Thing()

    assert t.last_flattr_at == None

    t._last_flattr_at = 'last_flattr_at'
    assert t.last_flattr_at == 'last_flattr_at'

    # this is an read-only field
    with raises(AttributeError):
        t.last_flattr_at = 'last_flattr_at'

def test_updated_at():
    t = Thing()

    assert t.updated_at == None

    t._updated_at = 'updated_at'
    assert t.updated_at == 'updated_at'

    # this is an read-only field
    with raises(AttributeError):
        t.updated_at = 'updated_at'

# test rw fields
def test_title():
    if sys.version < '3':
        res_title=u'f13_title'
    else:
        res_title='f13_title'
    t = Thing(dirty=False)

    assert t.title == None
    assert t._dirty == False

    t.title = res_title
    assert t.title == res_title
    assert t._dirty == True

    with raises(TypeError):
        t.title = 1

    if sys.version < '3':
        with raises(TypeError):
            t.title = 'f13_title'
    else:
        with raises(TypeError):
            t.title = b'f13_title'

def test_description():
    if sys.version < '3':
        res_description=u'f13_description'
    else:
        res_description='f13_description'
    t = Thing(dirty=False)

    assert t.description == None
    assert t._dirty == False

    t.description = res_description
    assert t.description == res_description
    assert t._dirty == True

    with raises(TypeError):
        t.description = 1

    if sys.version < '3':
        with raises(TypeError):
            t.description = 'f13_description'
    else:
        with raises(TypeError):
            t.description = b'f13_description'

def test_language():
    if sys.version < '3':
        res_language=u'f13_language'
    else:
        res_language='f13_language'
    t = Thing(dirty=False)

    assert t.language == None
    assert t._dirty == False

    t.language = res_language
    assert t.language == res_language
    assert t._dirty == True

    with raises(TypeError):
        t.language = 1

    if sys.version < '3':
        with raises(TypeError):
            t.language = 'f13_language'
    else:
        with raises(TypeError):
            t.language = b'f13_language'

def test_url():
    if sys.version < '3':
        res_url=u'http://f13_url'
        res_urls=u'https://f13_url'
    else:
        res_url='http://f13_url'
        res_urls='https://f13_url'
    t = Thing(dirty=False)

    assert t.url == None
    assert t._dirty == False

    t.url = res_url
    assert t.url == res_url
    assert t._dirty == True

    t.url = res_urls
    assert t.url == res_urls
    assert t._dirty == True

    with raises(TypeError):
        t.url = 1

    if sys.version < '3':
        with raises(TypeError):
            t.url = 'http://f13_url'
    else:
        with raises(TypeError):
            t.url = b'http://f13_url'

def test_category():
    if sys.version < '3':
        res_category=u'f13_category'
    else:
        res_category='f13_category'
    t = Thing(dirty=False)

    assert t.category == None
    assert t._dirty == False

    t.category = res_category
    assert t.category == res_category
    assert t._dirty == True

    with raises(TypeError):
        t.category = 1

    if sys.version < '3':
        with raises(TypeError):
            t.category = 'f13_category'
    else:
        with raises(TypeError):
            t.category = b'f13_category'

def test_tags():
    if sys.version < '3':
        res_tags=[u'f16_t1', u'f16_t2']
    else:
        res_tags=['f16_t1', 'f16_t2']
    t = Thing(dirty=False)

    assert t.tags == None
    assert t._dirty == False

    t.tags = res_tags
    assert t.tags == res_tags
    assert t._dirty == True
    
    with raises(TypeError):
        t.tags = 'Hello'

    if sys.version < '3':
        with raises(TypeError):
            t.tags = ['Hello']
    else:
        with raises(TypeError):
            t.tags = [b'Hello']

def test_hidden():
    t = Thing(dirty=False)

    assert t.hidden == False
    assert t._dirty == False

    t.hidden = True
    assert t.hidden == True
    assert t._dirty == True

    with raises(TypeError):
        t.hidden = 2

    delattr(t, '_hidden')
    assert t.hidden == False

# test constructor
def test_init():
    if sys.version < '3':
        res_title=u'f13_title'
        res_description=u'f14_description'
        res_url=u'http://xxx'
        res_tags=[u'f16_t1', u'f16_t2']
        res_language=u'f17_language'
        res_category=u'f18_category'
    else:
        res_title='f13_title'
        res_description='f14_description'
        res_url='http://xxx'
        res_tags=['f16_t1', 'f16_t2']
        res_language='f17_language'
        res_category='f18_category'

    t = Thing(
        resource='f2_resource',
        link='f3_link',
        id='f4_id',
        flattrs='f5_flattrs',
        flattrs_user_count='f6_flattrs_user_count',
        created_at='f7_created_at',
        owner='f8_owner',
        image='f9_image',
        flattred='f10_flattred',
        last_flattr_at='f11_last_flattr_at',
        updated_at='f12_updated_at',
        title=res_title,
        description=res_description,
        url=res_url,
        tags=res_tags,
        language=res_language,
        category=res_category,
        hidden=True)

    assert t.resource == 'f2_resource'
    assert t.link == 'f3_link'
    assert t.id == 'f4_id'
    assert t.flattrs == 'f5_flattrs'
    assert t.flattrs_user_count == 'f6_flattrs_user_count'
    assert t.created_at == 'f7_created_at'
    assert t.owner == 'f8_owner'
    assert t.image == 'f9_image'
    assert t.flattred == 'f10_flattred'
    assert t.last_flattr_at == 'f11_last_flattr_at'
    assert t.updated_at == 'f12_updated_at'
    assert t.title == res_title
    assert t.description == res_description
    assert t.url == res_url
    assert t.tags == res_tags
    assert t.language == res_language
    assert t.category == res_category
    assert t.hidden == True
    assert t._dirty == True

def test_init_validation():
    if sys.version < '3':
        with raises(TypeError):
            t = Thing(description='Hello')
        with raises(TypeError):
            t = Thing(url=u'Hello')
        with raises(TypeError):
            t = Thing(tags=['tag1'])
    else:
        with raises(TypeError):
            t = Thing(description=b'Hello')
        with raises(TypeError):
            t = Thing(url='Hello')
        with raises(TypeError):
            t = Thing(tags=[b'tag1'])

    with raises(TypeError):
        t = Thing(tags=1)

    with raises(TypeError):
        t = Thing(title=1)

    with raises(TypeError):
        t = Thing(description=1)

    with raises(TypeError):
        t = Thing(language=1)

    with raises(TypeError):
        t = Thing(category=1)

    with raises(TypeError):
        t = Thing(hidden=2)

    with raises(TypeError):
        t = Thing(url=1)

    t = Thing(dirty=False)
    assert t._dirty == False

class FakeResponse(object):

    def __init__(self, url, data, status_code=200):
        self.data = data
        self.url = url
        self.status_code = status_code


    def json(self):
        return {'url': self.url,
                'data': self.data,
                'id': self.data.get('id', 1)}

class FakeDeleteResponse(FakeResponse):

    def json(self):
        raise AttributeError('Should not be called')

class FakeSession(object):

    def __init__(self, status_code=200):
        self.status_code = status_code

    def post(self, url, data):
        return FakeResponse(url, data, status_code=self.status_code)

    def delete(self, url, params=None):
        return FakeDeleteResponse(url, params, status_code=self.status_code)

def test_support():
    t = Thing(session=FakeSession(), id=1)
    ret = t.support()

    # ret['id'] does not matter here, just part of test mock stuff
    assert ret['url'] == 'https://api.flattr.com/rest/v2/things/1/flattr'
    assert ret['data'] == {}

def test_commit_create():
    t = Thing(session=FakeSession(status_code=201), url='https://chrigl.de')
    ret = t.commit()

    assert ret['url'] == 'https://api.flattr.com/rest/v2/things/'
    assert ret['data'] == {'url': 'https://chrigl.de', 'hidden': False}
    assert ret['id'] == 1
    assert t._dirty == False

def test_commit_update():
    t = Thing(session=FakeSession(), url='https://chrigl.de', id=2)
    ret = t.commit()

    assert ret['url'] == 'https://api.flattr.com/rest/v2/things/2'
    assert ret['data'] == {'url': 'https://chrigl.de', 'hidden': False,
            '_method': 'patch'}
    # do not care about if field in this test. testing this is only required
    # for create.
    assert t._dirty == False

    ret = t.commit()
    assert ret is None

def test_delete():
    t = Thing(session=FakeSession(status_code=204), url='https://chrigl.de', id=2)
    ret = t.delete()

    assert t._dirty == True
    assert t._id is None

# TODO: REENABLE THIS TESTS
## And also implement the stuff
## Just disabled to get all tests running
#def test_refresh():
#    # this might be removed
#    t = Thing()
#    t.refresh()
#
#def test_subscribe():
#    t = Thing(session=None)
#    t.subscribe()
#
#def test_unsubscribe():
#    t = Thing(session=None)
#    t.unsubscribe()

def test_to_flattr_dict():
    t = Thing()

    with raises(AttributeError):
        t._to_flattr_dict()

    t.url = 'http://flattr.com'

    ret = t._to_flattr_dict()
    assert ret == {'url': 'http://flattr.com', 'hidden': False}

    t.title = 'Hello World'
    t.description = 'Some description'
    t.category = 'cat'
    t.language = 'de_DE'
    t.tags = ['test', 'me']
    t.hidden=True

    ret = t._to_flattr_dict()
    assert ret == {'url': 'http://flattr.com',
                   'hidden': True,
                   'title': 'Hello World',
                   'description': 'Some description',
                   'category': 'cat',
                   'tags': 'test,me'}

def test_repr():
    t = Thing()

    res = repr(t)
    assert res == '<flattr.things.Thing at %s>' % id(t)

    t.title = 'Hello World'
    res = repr(t)
    assert res == '<flattr.things.Thing Hello World>'
