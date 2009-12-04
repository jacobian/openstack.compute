from cloudservers import Image
from .fakeserver import FakeServer
from .utils import assert_isinstance
import nose.tools as nt

cs = FakeServer()

def test_list_images():
    il = cs.images.list()
    [assert_isinstance(i, Image) for i in il]
    
def test_get_image_details():
    i = cs.images.get(1)
    assert_isinstance(i, Image)
    nt.assert_equal(i.id, 1)
    nt.assert_equal(i.name, 'CentOS 5.2')
    
def test_create_image():
    i = cs.images.create(server=1234, name="Just in case")
    assert_isinstance(i, Image)
    
def test_delete_image():
    cs.images.delete(1)