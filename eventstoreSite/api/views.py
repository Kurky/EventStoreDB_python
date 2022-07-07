from esdbclient import EsdbClient
from urllib.parse import *
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .command import createCommand


def index(request):
    return HttpResponse("This is my eventStore project. Matej Kuráň")


@csrf_exempt
def eventCommand(request):
    if request.method == 'POST':
        # connecting
        client = EsdbClient(uri='localhost:2113')
        parameters = json.loads(request.body)
        if 'stream_name' in parameters and 'expected_position' in parameters and 'events' in parameters:
            events = parameters['events']
            for i in events:
                event = events[i]
                commit_positions = []
                if 'type' in event and 'data' in event and 'metadata' in event:
                    commit_position = createCommand(client, parameters['stream_name'], parameters['expected_position'], event['type'], event['data'], event['metadata'])
                    commit_positions.append(commit_position)
                x = {"commit_positions": commit_positions}
                string = json.dumps(x, default=str)
                string = string.replace(',', '')
                return HttpResponse(string, content_type="application/json")
            else:
                x = {"error": 'bad event json format'}
        else:
            x = {"error": 'bad stream json format'}
        string = json.dumps(x, default=str)
        string = string.replace(',', '')
        return HttpResponse(string, content_type="application/json")
    else:
        x = {"error": "no POST method"}
        string = json.dumps(x, default=str)
        string = string.replace(',', '')
        return HttpResponse(string, content_type="application/json")


def eventQuery(request):
    if request.method == 'GET':
        # connecting
        client = EsdbClient(uri='localhost:2113')
        # geting_parameters
        parameters = dict(parse_qs(urlsplit(request.get_raw_uri()).query))

    return HttpResponse("event_query")
