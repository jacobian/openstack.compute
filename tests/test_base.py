import cloudservers.base
import nose.tools as nt
from .fakeserver import FakeServer
from cloudservers import Flavor

cs = FakeServer()

def test_resource_repr():
    r = cloudservers.base.Resource(None, dict(foo="bar", baz="spam"))
    nt.assert_equal(repr(r), "<Resource baz=spam, foo=bar>")
    
def test_getid():
    nt.assert_equal(cloudservers.base.getid(4), 4)
    class O(object):
        id = 4
    nt.assert_equal(cloudservers.base.getid(O), 4)
    
def test_resource_lazy_getattr():
    f = Flavor(cs.flavors, {'id': 1})
    nt.assert_equal(f.name, '256 MB Server')