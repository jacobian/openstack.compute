import mock
import cloudservers.flavors
from nose.tools import *

def test_list_flavors():
    fake_client = mock.Mock()
    fake_client.get.return_value = (None, {
        'flavors': [
            {'id':'1', 'name':'one', 'ram': 123, 'disk': 456},
            {'id':'2', 'name':'two', 'ram': 789, 'disk': 987},
        ]
    })
    fm = cloudservers.flavors.FlavorManager(fake_client)
    flavors = fm.list()
    fake_client.get.assert_called_with('/flavors/detail')
    assert_equal(flavors[0].name, 'one')
    assert_equal(flavors[1].ram, 789)

def test_get_flavors():
    fake_client = mock.Mock()
    fake_client.get.return_value = (None, {
        'flavor': {'id':'1', 'name':'one', 'ram': 123, 'disk': 456},
    })
    fm = cloudservers.flavors.FlavorManager(fake_client)
    flavor = fm.get(1)
    fake_client.get.assert_called_with('/flavors/1')
    assert_equal(flavor.name, 'one')
    assert_equal(flavor.ram, 123)
    assert_equal(str(flavor), "<Flavor: one>")