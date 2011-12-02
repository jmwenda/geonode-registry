# Create your views here.
from registry.models import GeoNodeInstance, GeoNodeStatus
from django.http import HttpResponse, HttpResponseNotAllowed
import simplejson as json
import datetime

# Function to extract a subset of a dictionary. Found at:
# http://code.activestate.com/recipes/115417-subset-of-a-dictionary/
extract = lambda keys, dict: reduce(lambda x, y: x.update({y[0]:y[1]}) or x,
                                            map(None, keys, map(dict.get, keys)), {})


def geonode(request):
    if request.method != "POST":
        return HttpResponseNotAllowed("Only POST requests with JSON payload are accepted.")

    # Get the current datetime to be used in created_at or updated fields.
    right_now = datetime.datetime.utcnow()

    data = json.loads(request.raw_post_data)

    # Get the subset of the data that corresponds to the instance.
    instance_data = extract(['name', 'url', 'geoserver_base_url', 'geonetwork_base_url'], data)
    instance_data['created_at'] = right_now
    instance, created = GeoNodeInstance.objects.get_or_create(url=data['url'], defaults=instance_data)
    GeoNodeInstance.objects.filter(id=instance.id).update(**instance_data)

    status_data = extract(['map_count', 'layer_count', 'backup_date', 'faulty_layers', 'faulty_maps'], data)
    status = GeoNodeStatus.objects.create(instance=instance)
    status_data['created_at'] = right_now
    GeoNodeStatus.objects.filter(id=status.id).update(**status_data)

    output = {'instance': instance.id, 'status': status.id}
    return HttpResponse(json.dumps(output))
