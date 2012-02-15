from django.core.management.base import BaseCommand
from registry.models import GeoNodeInstance,GeoNodeFailure
import urllib
def ping(url):
    a=urllib.urlopen(url)
    return a.getcode()
   
def save(node):
    #we get the specifi GeoNodeInstance
    instance = GeoNodeInstance.objects.get(url=node['url'])
    GeoNodeFailure.objects.get_or_create(instance=instance, defaults=node)    
 
def ping_geonodes():
    '''This is the method that traverses the registered instances and checks to see if they are up and running'''
    geonodes = GeoNodeInstance.objects.all()
    for geonode in geonodes:
        status = {}
        status['code'] = ping(geonode.url)
        status['url'] = geonode.url
        status['mapscode'] = ping(geonode.url+'maps/search')
        status['datacode'] = ping(geonode.url+'data/search')
        for entity,code in status.iteritems():
            if code != 200:
                save(status)

class Command(BaseCommand):
    help = 'Checks all our registered GeoNodes to check if they are up and are in good health'
    args = '[none]'

    def handle(self, *args, **keywordargs):
        context = ping_geonodes()

