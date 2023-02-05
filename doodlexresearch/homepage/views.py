from django.shortcuts import render
from django.http import HttpResponse
from .traceroute import Async_calls
from .portscan_socket import PortScannerSocket
from django.views.decorators.csrf import csrf_exempt
import asyncio
import requests
import json

def traceroute_wrapper(endpoint):
    tr = Async_calls(endpoint)
    tr.perform_traceroute()
    asyncio.run(tr.main_calls())
    return tr.map_data()

def portscan_wrapper(endpoint,fromport,endport):
    sc = PortScannerSocket(adress = endpoint, fromport = fromport, endport = endport)
    sc.prepare_ports_format()
    result = sc.scan_ports()
    return result

def index(request):
    return render(request, "index.html")

@csrf_exempt
def traceroute(request):
    if request.method == 'POST':

        data=list(request.POST.items())
        ip_addr = data[0][1]
        result = traceroute_wrapper(ip_addr)
        result = json.dumps(result)

        return HttpResponse(result)

    return render(request, "traceroute.html")

@csrf_exempt
def scan_ports(request):
    if request.method == 'POST':

        data=list(request.POST.items())
        print(data)
        adress = data[0][1]
        fromport = data[1][1]
        endport = data[2][1]

        result = portscan_wrapper(adress, fromport, endport)
        result =json.dumps(result)

        return HttpResponse(result)

    return render(request, "port-scan.html")


