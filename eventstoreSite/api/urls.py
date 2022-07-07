from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('eventCommand/', views.eventCommand, name='eventCommand'),
    path('eventQuery/', views.eventQuery, name='eventQuery'),
]