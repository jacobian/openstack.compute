from . import base

class Server(base.Resource):
    def __repr__(self):
        return "<Server: %s>" % self.name
    
class ServerManager(base.Manager):
    resource_class = Server
    
    def get(self, server):
        return self._get("/servers/%s" % base.getid(server), "server")
        
    def list(self):
        return self._list("/servers/details", "servers")
        
    def create(self, name, image, flavor, ipgroup=None, meta=None, files=None):
        data = {"server": {
            "name": name,
            "imageId": base.getid(image),
            "flavorId": base.getid(flavor),
        }}
        if ipgroup:
            data["server"]["ipgroup"] = base.getid(ipgroup)
        if meta:
            data["server"]["metadata"] = meta
        if files:
            raise NotImplementedError
            
        return self._create("/servers", "server")
        
    def update(self, server, name=None, password=None):
        if name is None and password is None:
            return
        data = {"server": {}}
        if name:
            data["server"]["name"] = name
        if password:
            data["server"]["password"] = password
        return self._update("/servers/%s" % base.getid(server), data, "server")
        
    def delete(self, server):
        self._delete("/servers/%s" % base.getid(server))
