from esdbclient import EsdbClient
from urllib.parse import *
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .command import createCommand
from .query import query
import time


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
                    metadata = event['metadata']
                    metadata['crdate'] = int(time.time())
                    commit_position = createCommand(client, parameters['stream_name'], parameters['expected_position'],
                                                    event['type'], event['data'], metadata)
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
        parameters = dict(parse_qs(urlsplit(request.get_full_path()).query))
        minutes = 10

        returnedEvents = query(client, '4d4ef18a-a3ab-46f2-bf9f-31eeb699d5f0', None, True, 100)
        eventsToReturn = []
        for event in returnedEvents:
            metadata = json.loads(event.metadata.decode('utf-8'))
            if 'crdate' in metadata:
                if int(metadata['crdate']) > (int(time.time()) - (minutes * 60)):
                    eventsToReturn.append(event)
        x = {"events": eventsToReturn}
        string = json.dumps(x, default=str)
        string = string.replace(',', '')
        return HttpResponse(string, content_type="application/json")
    x = {"error": "no GET method"}
    string = json.dumps(x, default=str)
    string = string.replace(',', '')
    return HttpResponse(string, content_type="application/json")
