from django.db import models
from datetime import datetime
from geonode.maps.models import Map, Layer, MapLayer
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User


class GeoNodeInstances(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(verify_exists=False, null=True, blank=True)
    geoserver_base_url = models.URLField(verify_exists=False, null=True, blank=True)
    geonetwork_base_url = models.URLField(verify_exists=False, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "GeoNode"
        verbose_name_plural = "GeoNodes"
    
    def __unicode__(self):
        return self.name

    def from_json(self, data):
        try:
            self.name = data['name']
            self.url = data['url']
            self.geoserver_base_url = data['geoserver_base_url']
            self.geonetwork_base_url = data['geonetwork_base_url']
            self.created_at = datetime.utcnow()
            self.save()
            return self
        except:
            print sys.exc_info() 
            return None
class GeoNodeStatus(models.Model):
    instance = models.ForeignKey(GeoNodeInstances)
    layer_count = models.PositiveIntegerField(null=True, blank=True)
    map_count = models.PositiveIntegerField(null=True, blank=True)                                                                                        
    faulty_layers = models.PositiveIntegerField(null=True,blank=True)
    faulty_maps = models.PositiveIntegerField(null=True,blank=True)
    backup_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(null=True,blank=True)
    class Meta:
        verbose_name = "GeoNode's Status"
    def __unicode__(self):
        return self.instance
    def from_json(self,data):
        try:
            self.instance = GeoNodeInstances.objects.get(url=data['url'])
            self.layer_count = int(data['layer_count'])
            self.map_count = int(data['map_count'])
            self.faulty_layers = int(data['badlayers'])
            self.faulty_maps = int(data[' badmaps'])
            self.backup_date = datetime.utcfromtimestamp(data['backupdate'])
            self.created_at = datetime.utcnow()
            self.save()
            return self
        except:
            print sys.exc_info()
            return None


