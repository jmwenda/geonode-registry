from django.db import models
from datetime import datetime
from geonode.maps.models import Map, Layer, MapLayer
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User

class GeoNode(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(verify_exists=False, null=True, blank=True)
    #version = models.CharField(max_length=20, null=True, blank=True)
    geoserver_base_url = models.URLField(verify_exists=False, null=True, blank=True)
    geonetwork_base_url = models.URLField(verify_exists=False, null=True, blank=True)
    #admin = models.EmailField(null=True, blank=True)
    #owner = models.ForeignKey(User, null=True, blank=True)
    #description = models.TextField(null=True, blank=True)
    #area_of_interest = models.CharField(max_length=100, null=True, blank=True)
    layer_count = models.PositiveIntegerField(null=True, blank=True)
    map_count = models.PositiveIntegerField(null=True, blank=True)
    faulty_layers = models.PositiveIntegerField(null=True,blank=True)
    faulty_maps = models.PositiveIntegerField(null=True,blank=True)
    last_update = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "GeoNode"
        verbose_name_plural = "GeoNodes"
    
    def __unicode__(self):
        return self.name

    def from_json(self, data):
        try:
            self.name = data['name']
            self.url = data['url']
            #self.version = data['version']
            self.geoserver_base_url = data['geoserver_base_url']
            self.geonetwork_base_url = data['geonetwork_base_url']
            #self.admin = data['admin']
            #self.owner = data['owner']
            #self.description = data['description']
            #self.area_of_interest = data['area_of_interest']
            self.layer_count = int(data['layer_count'])
            self.map_count = int(data['map_count'])
            self.faulty_layers = int(data['badlayers'])
            self.faulty_maps = int(data['badmaps'])
            self.last_update = datetime.utcnow()
            self.save()
            return self
        except:
            print sys.exc_info() 
            return None

