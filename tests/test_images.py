import mock
import cloudservers.images
from nose.tools import *

def test_image_list():
    fake_client = mock.Mock()
    fake_client.get.return_value = (None, {
        'images': [
            {"id":1, "name":"CentOS 5.2", "updated": "2010-10-10T12:00:00Z", 
             "created": "2010-08-10T12:00:00Z", "status": "ACTIVE"},
            {"id":2, "name":"Server Backup", "updated": "2010-10-10T12:00:00Z", 
             "created": "2010-08-10T12:00:00Z", "status": "SAVING", "serverId": 1},
        ]
    })
    
    images = cloudservers.images.ImageManager(fake_client).list()
    fake_client.get.assert_called_with('/images/detail')
    assert_equal(images[0].name, "CentOS 5.2")
    assert_equal(images[1].status, "SAVING")
    # XXX serverID -> Server
    # XXX created -> datetime

def test_image_get():
    fake_client = mock.Mock()
    fake_client.get.return_value = (None, {
        'image': {
            "id":1, "name":"CentOS 5.2", "updated": "2010-10-10T12:00:00Z",
            "created": "2010-08-10T12:00:00Z", "status": "ACTIVE"
        }
    })
    
    image = cloudservers.images.ImageManager(fake_client).get(1)
    fake_client.get.assert_called_with('/images/1')
    assert_equal(str(image), "<Image: CentOS 5.2>")
    
def test_image_create():
    fake_client = mock.Mock()
    fake_client.post.return_value = (None, {
        'image': {
            "id":1, "name":"My Image", "updated": "2010-10-10T12:00:00Z",
            "created": "2010-08-10T12:00:00Z", "status": "SAVING", "serverId": 1
        }
    })

    image = cloudservers.images.ImageManager(fake_client).create("My Image", server=1)
    fake_client.post.assert_called_with("/images", data={'image': {'serverId': 1, 'name': 'My Image'}})
    
def test_image_delete():
    fake_client = mock.Mock()
    fake_client.delete.return_value = (None, None)
    cloudservers.images.ImageManager(fake_client).delete(1)
    fake_client.delete.assert_called_with("/images/1")
    