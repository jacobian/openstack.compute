from cloudservers import Server
from .fakeserver import FakeServer
from .utils import assert_isinstance
import nose.tools as nt

cs = FakeServer()

def test_list_servers():
    sl = cs.servers.list()
    cs.assert_called('GET', '/servers/detail')
    [assert_isinstance(s, Server) for s in sl]
    
def test_get_server_details():
    s = cs.servers.get(1234)
    cs.assert_called('GET', '/servers/1234')
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
    cs.assert_called('POST', '/servers')
    assert_isinstance(s, Server)
    
def test_update_server():
    s = cs.servers.get(1234)
    
    # Update via instance
    s.update(name='hi')
    cs.assert_called('PUT', '/servers/1234')
    s.update(name='hi', password='there')
    cs.assert_called('PUT', '/servers/1234')
    
    # Silly, but not an error
    s.update()
    
    # Update via manager
    cs.servers.update(s, name='hi')
    cs.assert_called('PUT', '/servers/1234')
    cs.servers.update(1234, password='there')
    cs.assert_called('PUT', '/servers/1234')
    cs.servers.update(s, name='hi', password='there')
    cs.assert_called('PUT', '/servers/1234')
    
def test_delete_server():
    cs.servers.delete(1234)
    cs.assert_called('DELETE', '/servers/1234')