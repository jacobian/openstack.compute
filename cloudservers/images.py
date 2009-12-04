from . import base

class Image(base.Resource):
    def __repr__(self):
        return "<Image: %s>" % self.name

class ImageManager(base.Manager):
    resource_class = Image
    
    def get(self, id):
        return self._get("/images/%s" % id, "image")
    
    def list(self):
        return self._list("/images/detail", "images")
    
    def create(self, name, server):
        data = {"image": {"serverId": base.getid(server), "name": name}}
        return self._create("/images", data, "image")
        
    def delete(self, image):
        self._delete("/images/%s" % getattr(image, 'id', int(image)))