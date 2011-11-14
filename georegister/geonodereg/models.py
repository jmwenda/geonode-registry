from django.db import models

# Create your models here.
class Instance(models.Model):
    domain = models.CharField(max_length=30)
    serverip = models.CharField(max_length=30)
    version = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    def __unicode__(self):
        return self.domain
class Log(models.Model):
    server = models.ForeignKey(Instance)
    detail = models.TextField()
    maps = models.IntegerField()
    layers = models.IntegerField()
    logtime = models.DateTimeField()
    def __unicode__(self):
        return self.server

