from django.conf.urls.defaults import *

urlpatterns = patterns('registry.views',
    (r'^geonode/(?P<geonode_id>[0-9]+)/$', 'geonode'),
    (r'^geonode/$', 'geonode'),
)
