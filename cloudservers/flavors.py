from . import base

class Flavor(base.Resource):
    def __repr__(self):
        return "<Flavor: %s>" % self.name

class FlavorManager(base.Manager):
    resource_class = Flavor
    
    def list(self):
        return self._list("/flavors/detail", "flavors")
        
    def get(self, id):
        return self._get("/flavors/%s" % id, "flavor")