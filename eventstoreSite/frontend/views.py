from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
import requests


# Create your views here.
def index(request):
    template = loader.get_template('index.html')
    response = requests.get('http://127.0.0.1:8000/api/eventQuery/')
    events = response.json()['events']
    stream_name = ''
    if events:
        stream_name = events[0]['stream_name']
    context = {
        'events': events,
        'stream_name': stream_name
    }
    return HttpResponse(template.render(context, request))
