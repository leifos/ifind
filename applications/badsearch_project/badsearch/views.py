from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
    context = RequestContext(request)
    context_dict = {'boldmessage': "I am bold font from the context"}

    return render_to_response('badsearch/index.html', context_dict, context)

def about(request):
    return HttpResponse("this is the about page")