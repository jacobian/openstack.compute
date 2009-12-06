from . import base

REBOOT_SOFT, REBOOT_HARD = 'SOFT', 'HARD'

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
    
    def reboot(self, type=REBOOT_SOFT):
        self.manager.reboot(self)
        
    def rebuild(self, image):
        self.manager.rebuild(self, image)
        
    def resize(self, flavor):
        self.manager.resize(self, flavor)
        
    def confirm_resize(self):
        self.manager.confirm_resize(self)
        
    def revert_resize(self):
        self.manager.revert_resize(self)
    
    @property
    def backup_schedule(self):
        return self.manager.api.backup_schedules.get(self)
    
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
        
        # Files are a slight bit tricky. They're passed in a "personality"
        # list to the POST. Each item is a dict giving a file name and the
        # base64-encoded contents of the file. We want to allow passing
        # either an open file *or* some contents as files here.
        if files:
            personality = body['server']['personality'] = []
            for filepath, file_or_string in files.items():
                if hasattr(file_or_string, 'read'):
                    data = file_or_string.read()
                else:
                    data = file_or_string
                personality.append({
                    'path': filepath,
                    'contents': data.encode('base64'),
                })
            
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
    
    def _action(self, action, server, info=None):
        """
        Perform a server "action" -- reboot/rebuild/resize/etc.
        """
        self.api.client.post('/servers/%s/action' % base.getid(server), body={action: info})
    
    def reboot(self, server, type=REBOOT_SOFT):
        self._action('reboot', server, {'type':type})
        
    def rebuild(self, server, image):
        self._action('rebuild', server, {'imageId': base.getid(image)})

    def resize(self, server, flavor):
        self._action('resize', server, {'flavorId': base.getid(flavor)})
        
    def confirm_resize(self, server):
        self._action('confirmResize', server)
        
    def revert_resize(self, server):
        self._action('revertResize', server)        