import json,requests
from pprint import pprint
from wit import Wit
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

wit_access_token = "WEJRB35U2WDNGJNX5OFNYGBDJSGPFLXR"
client=Wit(access_token=wit_access_token)

@csrf_exempt
def fbchat(request):
	if request.method == 'GET':
		if request.GET['hub.verify_token'] == '49329792364':
			return HttpResponse(request.GET['hub.challenge'])
		else:
			return HttpResponse("Error,invalid token")
	else:
		user_msg=json.loads(request.body.decode('utf-8'))
		for entry in user_msg['entry']:
			for message in entry['messaging']:
				if 'message' in message:
					fbid= message['sender']['id']
					text= message['message']['text']
					pprint(client.message(text))
					postfb(fbid,text)

	return HttpResponse()

def postfb(fbid,text):
	post_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAXsQKdeWhYBANEnYdJxrkGclTfc7MaZCY4H6qrEoPttwn2t73zF3i6SsN5Q3FweR1w1v6QqyFVmchEWwnSHgELwKx70HTAulZAmEBG1rE2hsz0gtwqcZBCVhnsl2CdQz1jjn8kUmZBeUBj1I9bPimAlZBUzON9rvKcakaglp0AZDZD'
	reply_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":text}})
	requests.post(post_url,headers={"Content-Type":"application/json"},data=reply_msg)

