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
        if request.body:
            parameters = json.loads(request.body)
            if 'stream_name' in parameters and 'expected_position' in parameters and 'events' in parameters:
                events = parameters['events']
                for i in events:
                    event = events[i]
                    commit_positions = []
                    if 'type' in event and 'data' in event and 'metadata' in event:
                        metadata = event['metadata']
                        metadata['crdate'] = int(time.time())
                        commit_position = createCommand(client, parameters['stream_name'],
                                                        parameters['expected_position'],
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
            commit_position = createCommand(client, '4d4ef18a-a3ab-46f2-bf9f-31eeb699d5f0', 0, 'OrderCreated',
                                            {"count": 10, "price": 25}, {"crdate": int(time.time())})
            x = {"commit_positions": commit_position}
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
        limit = 10
        position = None
        stream = '4d4ef18a-a3ab-46f2-bf9f-31eeb699d5f0'
        backwards = True
        if 'newerThan' in parameters: minutes = int(parameters['newerThan'][0])
        if 'limit' in parameters: limit = int(parameters['limit'][0])
        if 'position' in parameters: position = int(parameters['position'][0])
        if 'stream' in parameters: stream = parameters['stream'][0]
        if 'backwards' in parameters: backwards = bool(parameters['backwards'][0])
        returnedEvents = query(client, stream, position, backwards, limit)
        eventsToReturn = []
        for event in returnedEvents:
            metadata = json.loads(event.metadata.decode('utf-8'))
            if 'crdate' in metadata:
                if int(metadata['crdate']) > (int(time.time()) - (minutes * 60)):
                    jsonEvent = {'type': event.type, 'data': json.loads(event.data.decode('utf-8')),
                                 'metadata': metadata,
                                 'stream_name': event.stream_name, 'stream_position': event.stream_position,
                                 'commit_position': event.commit_position}
                    eventsToReturn.append(jsonEvent)
        x = {"events": eventsToReturn}
        string = json.dumps(x, default=str)
        return HttpResponse(string, content_type="application/json")
    x = {"error": "no GET method"}
    string = json.dumps(x, default=str)
    string = string.replace(',', '')
    return HttpResponse(string, content_type="application/json")
