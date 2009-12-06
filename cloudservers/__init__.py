from __future__ import absolute_import

__version__ = ('1.0a1')

from .client import CloudServersClient
from .flavors import FlavorManager, Flavor
from .images import ImageManager, Image
from .servers import ServerManager, Server
from .ipgroups import IPGroupManager, IPGroup
from .exceptions import *

class CloudServers(object):
    def __init__(self, username, apikey):
        self.client = CloudServersClient(username, apikey)
        self.flavors = FlavorManager(self)
        self.images = ImageManager(self)
        self.servers = ServerManager(self)
        self.ipgroups = IPGroupManager(self)
        
    def authenticate(self):
        self.client.authenticate()