from . import base

class Flavor(base.Resource):
    def __repr__(self):
        return "<Flavor: %s>" % self.name

class FlavorManager(base.ManagerWithFind):
    resource_class = Flavor
    
    def list(self):
        return self._list("/flavors/detail", "flavors")
        
    def get(self, flavor):
        return self._get("/flavors/%s" % base.getid(flavor), "flavor")