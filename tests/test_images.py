from cloudservers import Image
from .fakeserver import FakeServer
from .utils import assert_isinstance
import nose.tools as nt

cs = FakeServer()

def test_list_images():
    il = cs.images.list()
    cs.assert_called('GET', '/images/detail')
    [assert_isinstance(i, Image) for i in il]
    
def test_get_image_details():
    i = cs.images.get(1)
    cs.assert_called('GET', '/images/1')
    assert_isinstance(i, Image)
    nt.assert_equal(i.id, 1)
    nt.assert_equal(i.name, 'CentOS 5.2')
    
def test_create_image():
    i = cs.images.create(server=1234, name="Just in case")
    cs.assert_called('POST', '/images')
    assert_isinstance(i, Image)
    
def test_delete_image():
    cs.images.delete(1)
    cs.assert_called('DELETE', '/images/1')
    
def test_find():
    i = cs.images.find(name="CentOS 5.2")
    nt.assert_equal(i.id, 1)
    cs.assert_called('GET', '/images/detail')
    
    iml = cs.images.findall(status='SAVING')
    nt.assert_equal(len(iml), 1)
    nt.assert_equal(iml[0].name, 'My Server Backup')