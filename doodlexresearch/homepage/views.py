from django.shortcuts import render
from django.http import HttpResponse
from .traceroute import Async_calls
from django.views.decorators.csrf import csrf_exempt
import asyncio
import requests
import json

def traceroute_wrapper(endpoint):
    tr = Async_calls(endpoint)
    tr.perform_traceroute()
    asyncio.run(tr.main_calls())
    return tr.map_data()

def index(request):
    return render(request, "index.html")

# CSRF should take longer to make it right

@csrf_exempt
def traceroute(request):
    if request.method == 'POST':
        # reading the request
        data=list(request.POST.items())
        # getting the ip adress
        ip_addr = data[0][1]
        # performing the traceroute
        result = traceroute_wrapper(ip_addr)
        # from list of dictionaries to json
        result = json.dumps(result)
        return HttpResponse(result)


    return render(request, "traceroute.html")

    
"""
def submit_request(request):
    pass

"""

