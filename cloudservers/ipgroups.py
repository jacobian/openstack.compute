from . import base

class IPGroup(base.Resource):
    def __repr__(self):
        return "<IP Group: %s>" % self.name

    def delete(self):
        self.manager.delete(self)

class IPGroupManager(base.ManagerWithFind):
    resource_class = IPGroup
    
    def list(self):
        return self._list("/shared_ip_groups/detail", "sharedIpGroups")
        
    def get(self, id):
        return self._get("/shared_ip_groups/%s" % id, "sharedIpGroup")
    
    def create(self, name, server):
        data = {"sharedIpGroup": {"name": name, "server": base.getid(server)}}
        return self._create('/shared_ip_groups', data, "sharedIpGroup")
    
    def delete(self, group):
        self._delete("/shared_ip_groups/%s" % base.getid(group))
