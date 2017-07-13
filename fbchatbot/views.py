import json,requests
from pprint import pprint
from wit import Wit
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

wit_access_token = "WEJRB35U2WDNGJNX5OFNYGBDJSGPFLXR"
@csrf_exempt
def fbchat(request):
	if request.method == 'GET':
		if request.GET['hub.verify_token'] == '3425896715':
			return HttpResponse(request.GET['hub.challenge'])
		else:
			return HttpResponse("Error,invalid token")
	else:
		user_msg=json.loads(request.body.decode('utf-8'))
		for entry in user_msg['entry']:
			for message in entry['messaging']:
				fb_id= message['sender']['id']
				if message.get('message'):
					if 'text' in message['message']:
						#handling emojis parts
						if type(message['message']['text'])== bytes:
							message['message']['text']=str(message['message']['text'],"utf-8",errors="ignore")
						else:
							message['message']['text']=str(message['message']['text'])
						text=message['message']['text']
					else:
						#this part will handle the attachement parts for example like button,images etc
						text="You liked me"	
						postfb(fb_id,text)
						break # so that api call just happens once and then it exits.

					client.run_actions(session_id=fb_id,message=text)
	return HttpResponse()

def postfb(fb_id,text):
	post_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAXsQKdeWhYBANEnYdJxrkGclTfc7MaZCY4H6qrEoPttwn2t73zF3i6SsN5Q3FweR1w1v6QqyFVmchEWwnSHgELwKx70HTAulZAmEBG1rE2hsz0gtwqcZBCVhnsl2CdQz1jjn8kUmZBeUBj1I9bPimAlZBUzON9rvKcakaglp0AZDZD'
	reply_msg = json.dumps({"recipient":{"id":fb_id}, "message":{"text":text}})
	requests.post(post_url,headers={"Content-Type":"application/json"},data=reply_msg)

def send(request,response):
	fb_id=request['session_id']
	if request['entities']:
		text=str(response['text'])
		fresh_text=[]
		for i in range(2,len(text)-1):
			fresh_text.append(text[i])
		fresh_text = "".join(fresh_text)
		postfb(fb_id,fresh_text)
	else:
		default_text="Sorry I don't Understand please retry some other value!! :("
		postfb(fb_id,default_text)

actions = {
    'send': send,
}
client=Wit(access_token=wit_access_token,actions=actions)
