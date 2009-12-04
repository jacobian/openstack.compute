from .client import CloudServersClient
from .flavors import FlavorManager, Flavor
from .images import ImageManager, Image
from .servers import ServerManager, Server

class CloudServers(object):
    def __init__(self, username, apikey):
        self.client = CloudServersClient(username, apikey)
        self.flavors = FlavorManager(self)
        self.images = ImageManager(self)
        self.servers = ServerManager(self)