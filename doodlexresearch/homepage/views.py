from django.shortcuts import render

def index(request):
    return render(request, "index.html")

def traceroute(request):
    if request.POST:
        pass
    return render(request, "traceroute.html")

    
"""
def submit_request(request):
    pass

"""

