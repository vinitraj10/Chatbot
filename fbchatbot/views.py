import json,requests,datetime
from pprint import pprint
from wit import Wit
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from fbchatbot.chats.functions import(
	master_post_fb,
	greet_post_fb,
	post_weather_fb,
	askLocation,
	getWeather,
	cleaning_text
)

wit_access_token = "WIT_TOKEN"
@csrf_exempt
def fbchat(request):
	if request.method == 'GET':
		if request.GET['hub.verify_token'] == '3425896715':
			return HttpResponse(request.GET['hub.challenge'])
		else:
			return HttpResponse("Error,invalid token")
	else:
		user_msg=json.loads(request.body.decode('utf-8'))
		#pprint(user_msg)
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
						client.run_actions(session_id=fb_id,message=text)
					else:
						#this part will handle the attachement parts for example like button,images etc
						if 'coordinates' in message['message']['attachments'][0]['payload']:
							location=message['message']['attachments'][0]['payload']['coordinates']
							getWeather(location['lat'],location['long'],fb_id)
							
						else:
							text="You liked me"	
							master_post_fb(fb_id,text)
							break # so that api call just happens once and then it exits.

	return HttpResponse()



def send(request,response):
	fb_id=request['session_id']
	#pprint(request)
	user_details_url = "https://graph.facebook.com/v2.6/%s"%fb_id
	user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':'EAAXsQKdeWhYBANEnYdJxrkGclTfc7MaZCY4H6qrEoPttwn2t73zF3i6SsN5Q3FweR1w1v6QqyFVmchEWwnSHgELwKx70HTAulZAmEBG1rE2hsz0gtwqcZBCVhnsl2CdQz1jjn8kUmZBeUBj1I9bPimAlZBUzON9rvKcakaglp0AZDZD'}
	user_details = requests.get(user_details_url, user_details_params).json()
	pprint(user_details)
	if request['entities']:
		text=str(response['text'])
		text=cleaning_text(text)
		intent_type= request['entities']['intent'][0]['value']      #Storing intent type for user interactions for different intents.
		if intent_type == 'greet':
			text="Hey " + str(user_details['first_name']) + " This is my beta version,I can only find weather condition,but soon I will try to learn more things to become more useful for you :-) :)"
			greet_post_fb(fb_id,text)
		elif intent_type=='weather':
			askLocation(fb_id)
		else:
			master_post_fb(fb_id,text)
	else:
		default_text="Sorry I don't Understand please retry some other value!! :("
		master_post_fb(fb_id,default_text)

actions = {
    'send': send,
}
client=Wit(access_token=wit_access_token,actions=actions)
