from cloudservers import Flavor
from .fakeserver import FakeServer
from .utils import assert_isinstance
import nose.tools as nt

cs = FakeServer()

def test_list_flavors():
    fl = cs.flavors.list()
    cs.assert_called('GET', '/flavors/detail')
    [assert_isinstance(f, Flavor) for f in fl]
    
def test_get_flavor_details():
    f = cs.flavors.get(1)
    cs.assert_called('GET', '/flavors/1')
    assert_isinstance(f, Flavor)
    nt.assert_equal(f.ram, 256)
    nt.assert_equal(f.disk, 10)
    
def test_find():
    f = cs.flavors.find(ram=256)
    cs.assert_called('GET', '/flavors/detail')
    nt.assert_equal(f.name, '256 MB Server')
    
    f = cs.flavors.find(disk=20)
    nt.assert_equal(f.name, '512 MB Server')
    
    f = cs.flavors.find(disk=12345)
    nt.assert_equal(f, None)