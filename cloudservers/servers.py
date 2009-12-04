from . import base

class Server(base.Resource):
    def __repr__(self):
        return "<Server: %s>" % self.name
        
    def delete(self):
        self.manager.delete(self)
        
    def update(self, name=None, password=None):
        self.manager.update(self, name, password)
    
class ServerManager(base.Manager):
    resource_class = Server
    
    def get(self, server):
        return self._get("/servers/%s" % base.getid(server), "server")
        
    def list(self):
        return self._list("/servers/detail", "servers")
        
    def create(self, name, image, flavor, ipgroup=None, meta=None, files=None):
        body = {"server": {
            "name": name,
            "imageId": base.getid(image),
            "flavorId": base.getid(flavor),
        }}
        if ipgroup:
            body["server"]["sharedIpGroupId"] = base.getid(ipgroup)
        if meta:
            body["server"]["metadata"] = meta
        if files:
            raise NotImplementedError
            
        return self._create("/servers", body, "server")
        
    def update(self, server, name=None, password=None):
        if name is None and password is None:
            return
        body = {"server": {}}
        if name:
            body["server"]["name"] = name
        if password:
            body["server"]["adminPass"] = password
        self._update("/servers/%s" % base.getid(server), body)
        
    def delete(self, server):
        self._delete("/servers/%s" % base.getid(server))
