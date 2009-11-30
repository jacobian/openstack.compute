import cloudservers.base
from nose.tools import *

def test_resource_repr():
    r = cloudservers.base.Resource(None, dict(foo="bar", baz="spam"))
    assert_equal(repr(r), "<Resource baz=spam, foo=bar>")
    
def test_getid():
    assert_equal(cloudservers.base.getid(4), 4)
    class O(object):
        id = 4
    assert_equal(cloudservers.base.getid(O), 4)