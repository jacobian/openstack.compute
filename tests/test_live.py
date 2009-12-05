import os
import functools
import cloudservers
import time
from nose.plugins.skip import SkipTest

TESTABLE = 'CLOUD_SERVERS_USERNAME' in os.environ and 'CLOUD_SERVERS_API_KEY' in os.environ

if TESTABLE:
    cs = cloudservers.CloudServers(
        os.environ['CLOUD_SERVERS_USERNAME'],
        os.environ['CLOUD_SERVERS_API_KEY']
    )

def live(test):
    @functools.wraps(test)
    def _test():
        if not TESTABLE:
            raise SkipTest('no creds in environ')
        test()
    return _test

@live
def test_create_destroy():
    # Find the Ubuntu 9.10 image
    for im in cs.images.list():
        if im.name == 'Ubuntu 9.10 (karmic)':
            break
    
    # Find the 256 MB RAM flavor
    for flav in cs.flavors.list():
        if flav.ram == 256:
            break
    
    # Boot it.
    s = cs.servers.create('testserver', im, flav)
    while s.status != 'ACTIVE':
        time.sleep(10)
        s.get()
        
    # Destroy it.
    s.delete()