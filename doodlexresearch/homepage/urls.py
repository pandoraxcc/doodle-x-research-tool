from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('traceroute/', views.traceroute, name='traceroute'),
    path('scanports/', views.scan_ports, name='scanports'),
    path('discovery/', views.discover_network, name='discovery'),
]
