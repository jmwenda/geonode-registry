from registry.models import GeoNodeInstance, GeoNodeStatus
from registry.views import extract
from django.test.client import Client
from django.test import TestCase
import json

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

    data = json.loads(response.content)
    msg = 'Expected for find instance in a JSON dict if operation is successful'
    assert 'instance' in data, msg

    instance = GeoNodeInstance.objects.get(id=data['instance'])

    assert instance.__unicode__() is not None

    instance_data = extract(['name', 'url', 'geoserver_base_url', 'geonetwork_base_url'], post_data)

    for key, value in instance_data.items():
        actual_value = getattr(instance, key)
        msg = 'Expected "%s" but got "%s" for the "%s" attribute' % (value, actual_value, key)
        assert actual_value == value, msg

    msg = 'Expected to find status in response'
    assert 'status' in data,msg

    status = GeoNodeStatus.objects.get(id=data['status'])
    assert status.__unicode__() is not None

    status_data = extract(['layer_count', 'map_count', 'faulty_maps', 'faulty_layers', 'backup_date'], post_data)
 
    for key, value in status_data.items():
        actual_value = getattr(status, key)
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
                      'faulty_layers': 10,
                      'faulty_maps': 1,
                      'backup_date': None,
                      }
 
    def testNewInstance(self):
        """Check a new instance and status are created correctly.
        """
        new_instance(self.post_data)

        msg = "There should only be one instance created so far."
        assert GeoNodeInstance.objects.count()==1, msg


    def testInstanceCanBeRetreived(self):
        """Check that instance is not duplicated after a susequent request.
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
        """Check GET requests are marked as not allowed.
        """
        c = Client()
        response = c.get('/registry/geonode/')
        msg = "Expected 405 error code but got %s" % response.status_code
        assert response.status_code == 405, msg
