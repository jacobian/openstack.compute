from cloudservers import Flavor
from .fakeserver import FakeServer
from .utils import assert_isinstance
import nose.tools as nt

cs = FakeServer()

def test_list_flavors():
    fl = cs.flavors.list()
    [assert_isinstance(f, Flavor) for f in fl]
    
def test_get_flavor_details():
    f = cs.flavors.get(1)
    assert_isinstance(f, Flavor)
    nt.assert_equal(f.ram, 256)
    nt.assert_equal(f.disk, 10)