from django.db import models
from datetime import datetime
import sys
from geonode.maps.models import Map, Layer, MapLayer
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User


class GeoNodeInstance(models.Model):
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


class GeoNodeStatus(models.Model):
    instance = models.ForeignKey(GeoNodeInstance)
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
