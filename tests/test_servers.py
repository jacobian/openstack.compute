from cloudservers import Server
from .fakeserver import FakeServer
from .utils import assert_isinstance
import nose.tools as nt

cs = FakeServer()

def test_list_servers():
    sl = cs.servers.list()
    [assert_isinstance(s, Server) for s in sl]
    
def test_get_server_details():
    s = cs.servers.get(1234)
    assert_isinstance(s, Server)
    nt.assert_equal(s.id, 1234)
    nt.assert_equal(s.status, 'BUILD')
    
def test_create_server():
    s = cs.servers.create(
        name = "My server",
        image = 1,
        flavor = 1,
        meta = {'foo': 'bar'},
        ipgroup = 1,
    )
    assert_isinstance(s, Server)
    
def test_update_server():
    s = cs.servers.get(1234)
    
    # Update via instance
    s.update(name='hi')
    s.update(name='hi', password='there')
    
    # Silly, but not an error
    s.update()
    
    # Update via manager
    cs.servers.update(s, name='hi')
    cs.servers.update(1234, password='there')
    cs.servers.update(s, name='hi', password='there')
    
def test_delete_server():
    cs.servers.delete(1234)