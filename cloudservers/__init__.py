from .client import CloudServersClient
from .flavors import FlavorManager
from .images import ImageManager

class CloudServers(object):
    def __init__(self, username, apikey):
        self.client = CloudServersClient(username, apikey)
        self.flavors = FlavorManager(self.client)
        self.images = ImageManager(self.client)