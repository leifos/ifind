# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

import time
import json

def homepage(request):
	context = RequestContext(request)
	page_context = {'rendered_date_time': time.strftime("%H:%M:%S")}
	
	return render_to_response('testapp/homepage.html', page_context, context)

def latest_time(request):
	
	my_response = {}
	
	my_response['gold_count'] = 500
	my_response['current_time'] = time.strftime("%H:%M:%S")
	
	
	return HttpResponse(json.dumps(my_response), content_type="application/json")