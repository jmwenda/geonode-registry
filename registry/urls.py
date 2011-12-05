from django.conf.urls.defaults import *

urlpatterns = patterns('registry.views',
    (r'^geonode/$', 'geonode'),
)
