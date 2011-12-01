# Create your views here.
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_exempt, csrf_response_exempt
from django.http import HttpResponse

import simplejson as json

from registry.models import GeoNodeInstance,GeoNodeStatus

@csrf_exempt
def geonode(request, geonode_id=None):
    if(geonode_id != None and request.method == "GET"):
        geonode = get_object_or_404(GeoNodeInstance, pk=geonode_id)
        return HttpResponse(serializers.serialize("json", [geonode]))
    elif(geonode_id == None and request.method == "GET"):
        geonodes = GeoNodeInstance.objects.all()
        return HttpResponse(serializers.serialize("json", geonodes))
    elif( request.method == "POST"):
        data = json.loads(request.raw_post_data)
        instance = GeoNodeInstance.objects.get(url=data['url'])
        if instance is None:
            geonodeinstance = GeoNodeInstance()
            geonodeinstance.from_json(data)
        status = GeoNodeStatus()
        status.from_json(data)
        return HttpResponse(serializers.serialize("json", [status]))
    elif(geonode_id != None and request.method == "PUT"):
        data = json.loads(request.raw_post_data)
        geonode = GeoNodeInstance.objects.get(pk=geonode_id)
        geonode.from_json(data)
        return HttpResponse(serializers.serialize("json", [geonode]))
    elif(geonode_id != None and request.method == "DELETE"):
        geonode = GeoNodeInstance.objects.get(pk=geonode_id)
        geonode.delete()
        data = {'status': 'success', 'msg': 'geonode deleted'}
        return HttpResponse(json.dumps(data), mimetype='application/json')
    else:
        return HttpResponse("invalid request") 

