from registry.models import GeoNodeInstance
from registry.views import extract
from django.test.client import Client
from django.test import TestCase
import json
import datetime

def new_instance(post_data):
    """Send the post_data to the view and check the returned instance
    """
    c = Client()
    # Play a little bit with the headers so Django recognizes the 
    # post data as JSON and does not ignore it.
    response = c.post('/registry/geonode/',
                       json.dumps(post_data), "text/json", 
                       HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    msg = ('The insertion of a new record did not complete'
           'the server returned a HTTP %s error.' % response.status_code)
    assert response.status_code == 200, msg

    instance = GeoNodeInstance.objects.get()

    assert instance.__unicode__() == post_data['name']

    instance_data = extract(['name', 'url', 'geoserver_base_url', 'geonetwork_base_url'], post_data)

    for key, value in instance_data.items():
        actual_value = getattr(instance, key)
        msg = 'Expected "%s" but got "%s" for the "%s" attribute' % (value, actual_value, key)
        assert actual_value == value, msg



class TestRegistryViews(TestCase):

    def setUp(self):
        self.post_data = {
                      'name': 'geonode site',
                      'url': 'http://demo.geonode.org',
                      'geoserver_base_url': 'http://demo.geonode.org/geoserver',
                      'geonetwork_base_url': 'http://demo.geonode.org/geonetwork',
                      'layer_count': 100,
                      'map_count': 10,
                      'badlayers': 10,
                      'badmaps': 1,
                      'backupdate': None,
                      }
 
    def testNewInstance(self):
        """Check a new instance is created correctly.
        """
        new_instance(self.post_data)

        msg = "There should only be one instance created so far."
        assert GeoNodeInstance.objects.count()==1, msg


    def testInstanceCanBeRetreived(self):
        """Check that the same instance is updated after a second request.
        """
        new_instance(self.post_data)

        msg = "There should only be one instance created so far."
        assert GeoNodeInstance.objects.count()==1, msg

        post_data = self.post_data
        post_data['name'] = 'geonode site 2'
        new_instance(post_data)

        msg = "The registry could  not recognize this was the same instance by the url."
        assert GeoNodeInstance.objects.count()==1, msg


    def testGETisInvalid(self):
        """Check GET requests are marked as invalid.
        """
        c = Client()
        response = c.get('/registry/geonode/')
        msg = "Expected 405 error code but got %s" % response.status_code
        assert response.status_code == 405, msg
