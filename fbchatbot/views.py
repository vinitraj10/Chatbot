import json,requests
from pprint import pprint
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def fbchat(request):
	if request.method == 'GET':
		if request.GET['hub.verify_token'] == '49329792364':
			return HttpResponse(request.GET['hub.challenge'])
		else:
			return HttpResponse("Error,invalid token")
	else:
		user_msg=json.loads(request.body.decode('utf-8'))
		pprint(user_msg)

	return HttpResponse()