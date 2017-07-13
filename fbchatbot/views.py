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



def master_post_fb(fb_id,text):
	post_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAXsQKdeWhYBANEnYdJxrkGclTfc7MaZCY4H6qrEoPttwn2t73zF3i6SsN5Q3FweR1w1v6QqyFVmchEWwnSHgELwKx70HTAulZAmEBG1rE2hsz0gtwqcZBCVhnsl2CdQz1jjn8kUmZBeUBj1I9bPimAlZBUzON9rvKcakaglp0AZDZD'
	reply_msg = json.dumps({"recipient":{"id":fb_id}, "message":{"text":text}})
	requests.post(post_url,headers={"Content-Type":"application/json"},data=reply_msg)

def greet_post_fb(fb_id,text):
	post_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAXsQKdeWhYBANEnYdJxrkGclTfc7MaZCY4H6qrEoPttwn2t73zF3i6SsN5Q3FweR1w1v6QqyFVmchEWwnSHgELwKx70HTAulZAmEBG1rE2hsz0gtwqcZBCVhnsl2CdQz1jjn8kUmZBeUBj1I9bPimAlZBUzON9rvKcakaglp0AZDZD'
	reply_msg = json.dumps({
		"recipient":{"id":fb_id}, 
		"message":{
			"text":text,
			"quick_replies":[
				{
       			 "content_type":"location",
      			}
    		]
    	}
    }
 )
	requests.post(post_url,headers={"Content-Type":"application/json"},data=reply_msg)

def post_weather_fb(weather_report,weather_icon,fb_id):
	post_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAXsQKdeWhYBANEnYdJxrkGclTfc7MaZCY4H6qrEoPttwn2t73zF3i6SsN5Q3FweR1w1v6QqyFVmchEWwnSHgELwKx70HTAulZAmEBG1rE2hsz0gtwqcZBCVhnsl2CdQz1jjn8kUmZBeUBj1I9bPimAlZBUzON9rvKcakaglp0AZDZD'
	reply_msg = json.dumps({
		"recipient":{"id":fb_id},
		"message":{
			"text":weather_report,
			}
		}
	)
	requests.post(post_url,headers={"Content-Type":"application/json"},data=reply_msg)


def askLocation(fb_id):
	post_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAXsQKdeWhYBANEnYdJxrkGclTfc7MaZCY4H6qrEoPttwn2t73zF3i6SsN5Q3FweR1w1v6QqyFVmchEWwnSHgELwKx70HTAulZAmEBG1rE2hsz0gtwqcZBCVhnsl2CdQz1jjn8kUmZBeUBj1I9bPimAlZBUzON9rvKcakaglp0AZDZD'
	reply_msg = json.dumps({
		"recipient":{"id":fb_id}, 
		"message":{
			"text":'Please Share Your Location',
			"quick_replies":[
				{
       			 "content_type":"location",
      			}
    		]
    	}
    }
 )
	requests.post(post_url,headers={"Content-Type":"application/json"},data=reply_msg)


def getWeather(lat,lon,fb_id):
	appid='b1b15e88fa797225412429c1c50c122a1'
	url='http://samples.openweathermap.org/data/2.5/weather?lat=' + str(lat) + "&" + "lon=" + str(lon) + "&appid=" + str(appid) 
	result=requests.get(url).json()
	weather_report=result['weather'][0]['description']
	weather_icon = result['weather'][0]['icon']
	print(weather_icon)
	post_weather_fb(weather_report,weather_icon,fb_id)

def cleaning_text(text):
	fresh_text=[]
	for i in range(2,len(text)-1):
		fresh_text.append(text[i])
	fresh_text = "".join(fresh_text)
	return fresh_text

def send(request,response):
	fb_id=request['session_id']
	#pprint(request)
	if request['entities']:
		text=str(response['text'])
		text=cleaning_text(text)
		intent_type= request['entities']['intent'][0]['value']      #Storing intent type for user interactions for different intents.
		if intent_type == 'greet':
			greet_post_fb(fb_id,text)
		elif intent_type=='weather':
			text="santa banta hahahahahaha"	
			askLocation(fb_id)
	else:
		default_text="Sorry I don't Understand please retry some other value!! :("
		master_post_fb(fb_id,default_text)

actions = {
    'send': send,
}
client=Wit(access_token=wit_access_token,actions=actions)
