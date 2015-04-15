python-flattr
=============

python-flattr is a client library to the micro payment service flattr_. It
implements most aspects of the `flattr rest api`_. You may use it, to integrate
flattr_-Support into your python program. For example creating things_ for new
blog posts. Or you write some kind of podcatcher and want to automatically
flattr (support) each downloaded episode.

Features
--------

* create and update things
* delete things
* get things by id
* search things
* list things of a known user
* list your things
* list your subscriptions
* subscribe to things
* pause/resume subscriptions
* flattr/support things

Installation
------------

.. code-block:: python
   
   pip install flattr

Usage
-----

DISCLAIMER: The following code examples are python3. If you are using python2,
you have to pass unicodes especially to attributes of ``flattrclient.things.Thing``.


First of all. You need to get an auth token. The implementation is up to you,
with only little help of python-flattr.

Workflow to get the auth token
``````````````````````````````

Follow the `authorization workflow`_. First of all, `register your app`_ in your
user profile on flattr, to get the *Client ID* and *Client Secret*.

With this credentials you can set up an api-connection

.. code-block:: python
   
   >>> import flattrclient.oauth
   >>> auth_api = flattrclient.oauth.get()

You can call ``authorize`` to get the URL, you have to point your user to.

.. code-block:: python
   
   >>> auth_api.authorize(CLIENT_ID, 'flattr,thing,email,extendedread', 'http://localhost:8080')
   'https://flattr.com/oauth/authorize?scope=flattr%2Cthing%2Cemail%2Cextendedread&redirect_uri=http%3A%2F%2Flocalhost%3A8080&response_type=code&client_id=CLIENT_ID'

However, you decide which scopes_ you need.

You may want to listen to ``localhost:8080`` or whatever callback you used.
flattr_ will redirect the user to this URL, and send you (on success), a ``code``.
Pick this up and get the access token. This is also the only time, you need the
*Client Secret*.

.. code-block:: python
   
   >>> auth_api.set_auth(CLIENT_ID, CLIENT_SECRET)
   >>> auth_api.token(CODE, 'http://localhost:8080')
   'XXXXX'

The entire process of getting the ``code`` an requesting the token should not
take too long. Anyway, it is still fast enough, if you copying the code from
another terminal window and call ``token`` in an interactive session.

Working with python-flattr
``````````````````````````

In fact. The access token is the only thing you need to store somewhere.
From now on. You should be able to talk to the `flattr rest api`_. Give
it a try and get all things of the user ``flattr``

.. code-block:: python
   
   >>> import flattrclient.api
   >>> api = flattrclient.api.get(AUTH_TOKEN)
   >>> f = api.users('flattr')
   >>> f
   <flattrclient.user.User flattr>
   >>> things = list(f.get_things())
   [<flattrclient.things.Thing Bielefeld gibts wirklich! Zumindest im Fußball>,
    <flattrclient.things.Thing Tweet by @Flattr, 25 Feb>,
    ...]

That was fun. But what happened?

First, we introduced the session between flattr_ and us, using ``flattrclient.api.get``.
This is very likely always the first thing, you do. Currently I use
``requests.sessions.Session`` in the background, without any pooling.

Then we create a lightweight ``flattrclient.user.User``-object. This does not perform
any api-call. So if there is a typo, the next call (``get_things``), will cause
the error. If you want, to perform an api-call for the user, use
``api.users.get('flattr')``.

The nect call to ``f.get_things()`` returns all things as a generator. So to make
it more verbose here, we converted it into a list.  All things? Not really. By
default, the api only returns 30 results per page. But you can use ``count`` and
``page`` to override this.

.. code-block:: python
   
   >>> f.get_things(count=10, page=2)

You get page 2 of the results. Each page batched to 10 results.


Let's step back to the ``api``.  The api consits of a bunch of different other
apis, to which the ``request.session.Session`` object is passed.


``api.things``: Talk to flattrs things api. ``get``, ``lookup`` and ``search`` for
things.

``api.users``: Talk to flattrs user api. ``__call__`` and ``get``, described above.

``api.authenticated``: Talk to flattrs authenticated api. Which means... list
stuff of the authenticated user. ``get_activities``, ``get_flattrs``, ``get_things``
and ``get_subscriptions``.


However. You may want to create a new thing on flattr_.

.. code-block:: python
   
   >>> mything = api.things.new(url='http://example.com', title='crazy title')
   >>> mything
   <flattrclient.things.Thing craty title>
   >>> mything.description = 'Some more context'
   >>> mything.commit()

You should use ``api.things.new`` to get a new object of ``flattrclient.things.Thing``
because it again takes care of setting the session.


Same if you want to update one of your things.

.. code-block:: python
   
   >>> mythings = list(api.authenticated.get_things())
   >>> some_thing = mythings[0]
   >>> some_thing.title = 'Some new Title'
   >>> some_thing.commit()

You may not just create or update your own things_, but also flattr someones
stuff. Each thing you got by user, or fetch via ``api.things`` is supportable.

.. code-block:: python
   
   >>> thing = api.things.get('4085245')
   >>> thing
   <flattrclient.things.Thing chrigl/python-flattr on GitHub>
   >>> thing.support()
   {...}

Just supporting is not enough? Subscribe to the thing

.. code-block:: python
   
   >>> thing = api.things.get('4085245')
   >>> thing
   <flattrclient.things.Thing chrigl/python-flattr on GitHub>
   >>> thing.subscribe()
   {...}

There is also a ``unsubscribe`` and a ``pause_subscription``, which is a toggle
to pause and resume this subscription.


Feel free to use ``help`` on different stuff. Where it is much more useful to
use python3, since internaly some decorators are used, which results in
``*args, **kwargs``-argument-lists in python2.

Issues
------

You are welcome to file issues or pull requests on github_.

License
-------

Apache License 2.0

.. _flattr: https://flattr.com/
.. _`flattr rest api`: http://developers.flattr.net/
.. _`things`: http://developers.flattr.net/api/resources/things/
.. _`authorization workflow`: http://developers.flattr.net/api/#authorization
.. _`register your app`: http://flattr.com/apps/new
.. _scopes: http://developers.flattr.net/api/#scopes
.. _github: https://github.com/chrigl/python-flattr
