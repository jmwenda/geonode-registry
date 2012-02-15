from registry.models import GeoNodeInstance,GeoNodeStatus,FaultyLayer,GeoNodeFailure
from django.contrib import admin


admin.site.register(GeoNodeInstance)
admin.site.register(GeoNodeStatus)
admin.site.register(FaultyLayer)
admin.site.register(GeoNodeFailure)
