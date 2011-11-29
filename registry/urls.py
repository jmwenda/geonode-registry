from django.conf.urls.defaults import *

urlpatterns = patterns('geonode.geonodestate.views',
    (r'^geonode/(?P<geonode_id>[0-9]+)/$', 'geonode'),
    (r'^geonode/$', 'geonode'),
)
