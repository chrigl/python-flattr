from flattr.things import Thing
from flattr.subscriptions import Subscription

def test_subscription():
    subscription = Subscription(session='Hello World', created_at='now',
            started_at='yesterday', thing={'title': 'testing'}, ignore_me=1)

    assert subscription.active == True
    assert subscription._session == 'Hello World'
    assert subscription.created_at == 'now'
    assert subscription.started_at == 'yesterday'
    assert isinstance(subscription._thing, Thing)
    assert subscription._thing._session is subscription._session

    res = repr(subscription)
    assert res == '<flattr.subscriptions.Subscription testing>'

    subscription._thing = {'hello': 'world'}
    res = repr(subscription)
    assert res == '<flattr.subscriptions.Subscription at %s>' % id(subscription)

    delattr(subscription, '_thing')
    res = repr(subscription)
    assert res == '<flattr.subscriptions.Subscription at %s>' % id(subscription)
