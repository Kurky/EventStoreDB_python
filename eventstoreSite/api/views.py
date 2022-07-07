from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("This is my eventStore project. Matej Kuráň")


def eventCommand(request):
    return HttpResponse("event_command")


def eventQuery(request):
    return HttpResponse("event_query")
