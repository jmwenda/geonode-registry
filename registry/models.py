from django.db import models


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
    faulty_layers_count = models.PositiveIntegerField(null=True,blank=True)
    faulty_maps_count = models.PositiveIntegerField(null=True,blank=True)
    backup_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(null=True,blank=True)
    class Meta:
        verbose_name = "GeoNode's Status"
    def __unicode__(self):
        return 'Status of %s at %s' % (self.instance, self.created_at)
class FaultyLayer(models.Model):
    status = models.ForeignKey(GeoNodeStatus)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    reason = models.TextField(null=True,blank=True)
    def __unicode__(self):
        return 'Faulty Layers %s at %s' % (self.name,self.status)
