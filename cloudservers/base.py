"""
Base utilities to build API operation managers and objects on top of.
"""

class Manager(object):
    """
    Managers interact with a particular type of API (servers, flavors, images,
    etc.) and provide CRUD operations for them.
    """
    resource_class = None
    
    def __init__(self, client):
        self.client = client
        
    def _list(self, url, response_key):
        resp, body = self.client.get(url)
        return [self.resource_class(self, res) for res in body[response_key]]
    
    def _get(self, url, response_key):
        resp, body = self.client.get(url)
        return self.resource_class(self, body[response_key])
    
    def _create(self, url, data, response_key):
        resp, body = self.client.post(url, data=data)
        return self.resource_class(self, body[response_key])
        
    def _delete(self, url):
        resp, body = self.client.delete(url)
    
    def _update(self, url, data, response_key):
        resp, body = self.client.put(url, data=data)
        return self.resource_class(self, body[response_key])
    
class Resource(object):
    """
    A resource represents a particular instance of an object (server, flavor,
    etc). This is pretty much just a bag for attributes.
    """
    def __init__(self, manager, info):
        self.manager = manager
        for (k, v) in info.iteritems():
            setattr(self, k, v)
            
    def __repr__(self):
        reprkeys = sorted(k for k in self.__dict__.keys() if k[0] != '_' and k != 'manager')
        info = ", ".join("%s=%s" % (k, getattr(self, k)) for k in reprkeys)
        return "<%s %s>" % (self.__class__.__name__, info)
        
def getid(obj):
    """
    Abstracts the common pattern of allowing both an object or an object's ID
    (integer) as a parameter when dealing with relationships.
    """
    try:
        return obj.id
    except AttributeError:
        return int(obj)