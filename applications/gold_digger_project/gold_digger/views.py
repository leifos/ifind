from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

def home(request):

    context = RequestContext(request)
    return render_to_response('gold_digger/home.html', context)

def about(request):

    context = RequestContext(request)
    return render_to_response('gold_digger/about.html', context)

def leaderboards(request):

    context = RequestContext(request)
    return render_to_response('gold_digger/leaderboards.html', context)

def register(request):

    context = RequestContext(request)
    return render_to_response('gold_digger/register.html', context)

