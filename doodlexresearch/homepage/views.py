from django.shortcuts import render
from django.http import HttpResponse
from .traceroute import Traceroute_async
from .portscan_socket import PortScannerSocket
from .portscan_nmap import PortScannerTool
from .terminal_colors import BeautifyTerminal
from django.views.decorators.csrf import csrf_exempt
import asyncio
import os
import time
import requests
import json

def traceroute_wrapper(endpoint):
    tr = Traceroute_async(endpoint)
    tr.perform_traceroute()
    asyncio.run(tr.main_calls())
    
    return tr.map_data()

def portscan_wrapper_sockets(endpoint, fromport, endport):
    ps = PortScannerSocket(host=endpoint, fromport=fromport, endport=endport)
    ps.prepare_ports_format()
    status = ps.check_host_is_up_ping()

    if status:
        print(f'{BeautifyTerminal.OKGREEN}*** the host is up ***{BeautifyTerminal.ENDC}')
        print(f'{BeautifyTerminal.OKGREEN}*** running socket scanner ***{BeautifyTerminal.ENDC}')

        ps.scan_ports()
        result = ps.check_results()
    
    else:
        print(f'{BeautifyTerminal.WARNING}*** the host is down ***{BeautifyTerminal.ENC}')
        result = ps.open_ports
        
    return result


def portscan_wrapper_nmap(endpoint,fromport,endport):
    sc = PortScannerTool(host=endpoint, fromport=fromport, endport=endport)
    sc.prepare_port_format()
    status = sc.check_host_is_up_ping()

    if status:
        print(f'{BeautifyTerminal.OKGREEN}*** the host is up ***{BeautifyTerminal.ENDC}')
        print(f'{BeautifyTerminal.OKGREEN}*** running nmap scanner ***{BeautifyTerminal.ENDC}')

        sc.scan_ports()
        sc.prepare_results()
        result = sc.check_results()
    
    else:
        print(f'{BeautifyTerminal.WARNING}*** the host is down ***{BeautifyTerminal.ENDC}')
        sc.check_results()
        result = sc.open_ports

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

        local_hosts_types = ['0.0.0.0', '127.0.0.1', 'localhost']

        # reading data from the Post request
        host = data[0][1]
        fromport = data[1][1]
        endport = data[2][1]

        start_time = time.time()

        if host in local_hosts_types:
            print("0")
            result = portscan_wrapper_sockets(host, fromport, endport)
        
        else:
            print("1")
            result = portscan_wrapper_nmap(host, fromport, endport)

        # >>>  Testing different scenarios  <<< #:

        # Case1: Non sensitive and sensetive ports
        # result = [["55530", "localhsot", "port is open"], ["55531", "localhsot", "port is open"], ["55532", "localhsot", "port is open"], ["55533", "localhsot", "port is open"], ["55534", "localhsot", "port is open"], ["22", "localhsot", "port is open"]]
        
        # Case2: Sensitive ports
        # result = [["22", "localhsot", "port is open"], ["23", "localhsot", "port is open"], ["51", "localhsot", "port is open"], ["88", "localhsot", "port is open"], ["137", "localhsot", "port is open"]]
        
        # Case3: Sensitive port
        # result = [["69", "localhsot", "port is open"]]

        # Case4: Non sensitive port 
        # result = [["1337", "localhsot", "port is open"]]

        # Case5: No open ports
        # result = [["No open ports", "localhost", "There are no open ports from the given range 1: 65535 "]]

        # Case6: Error
        # result = [["Error: Host is down", "256.256.256.256", "An error occured during the scan, firewall blocked the connection or host 256.256.256.256 is down"]]
        
        # >>>  End of tests  <<< #:

        print("--- %s seconds ---" % (time.time() - start_time))

        result =json.dumps(result)
        print(result)

        return HttpResponse(result)

    return render(request, "port-scan.html")


