from . import base

class Server(base.Resource):
    def __repr__(self):
        return "<Server: %s>" % self.name
        
    def delete(self):
        self.manager.delete(self)
        
    def update(self, name=None, password=None):
        self.manager.update(self, name, password)
    
    def share_ip(self, ipgroup, address, configure=True):
        """
        Share an IP address from the given IP group onto this server.
        """
        self.manager.share_ip(self, ipgroup, address, configure)
    
    def unshare_ip(self, address):
        """
        Remove the shared address from this server.
        """
        self.manager.unshare_ip(self, address)
    
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

    def share_ip(self, server, ipgroup, address, configure=True):
        """
        Share an IP address from the given IP group onto this server.
        """
        server = base.getid(server)
        ipgroup = base.getid(ipgroup)
        body = {'shareIp': {'sharedIpGroupId': ipgroup, 'configureServer': configure}}
        self._update("/servers/%s/ips/public/%s" % (server, address), body)
        
    def unshare_ip(self, server, address):
        """
        Remove the shared address from this server.
        """
        server = base.getid(server)
        self._delete("/servers/%s/ips/public/%s" % (server, address))
