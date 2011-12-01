from geonode.maps.models import Map, Layer, MapLayer, Contact, ContactRole, Role
from registry.models import GeoNodeInstance,GeoNodeStatus
from django.contrib.contenttypes.models import ContentType
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.contenttypes import generic


admin.site.register(GeoNodeInstance)
admin.site.register(GeoNodeStatus)
