import json,requests,datetime
from pprint import pprint
from wit import Wit
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

wit_access_token = <wit_access_token>
@csrf_exempt
def fbchat(request):
	if request.method == 'GET':
		if request.GET['hub.verify_token'] == <verify_token>:
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
	post_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=<access_token>'
	reply_msg = json.dumps({"recipient":{"id":fb_id}, "message":{"text":text}})
	requests.post(post_url,headers={"Content-Type":"application/json"},data=reply_msg)

def greet_post_fb(fb_id,text):
	post_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=<access_token>'
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

def post_weather_fb(final_report,fb_id):
	post_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=<access_token>'
		reply_msg = json.dumps({
		"recipient":{"id":fb_id},
		"message":{
			"text":final_report,
			}
		}
	)
	requests.post(post_url,headers={"Content-Type":"application/json"},data=reply_msg)


def askLocation(fb_id):
	post_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=<access_token>'
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
	key="772973e281f73ebc401d23c974de0f09"
	url="https://api.darksky.net/forecast/"+str(key)+"/"+ str(lat) + "," + str(lon)
	#pprint(requests.get(url).json())
	result=requests.get(url).json()
	temp_max=int(((result['daily']['data'][0]['temperatureMax'])-32)*0.5555555555555556)
	temp_min=int(((result['daily']['data'][0]['temperatureMin'])-32)*0.5555555555555556)
	sunrise=datetime.datetime.fromtimestamp(int(result['daily']['data'][0]['sunriseTime'])).strftime('%H:%M:%S')
	sunset=datetime.datetime.fromtimestamp(int(result['daily']['data'][0]['sunsetTime'])).strftime('%H:%M:%S')
	timeZone=(result['timezone'])
	summary=result['hourly']['summary']
	final_report="Max temp : " + str(temp_max) + " °C \n" + "Min temp : " + str(temp_min) + " ° C \n" +"Sunrise time : " + str(sunrise) + "\n" +"Sunset time : " +str(sunset) + "\n" + "summary : " + str(summary)
	post_weather_fb(final_report,fb_id)

def cleaning_text(text):
	fresh_text=[]
	for i in range(2,len(text)-1):
		fresh_text.append(text[i])
	fresh_text = "".join(fresh_text)
	return fresh_text

def send(request,response):
	fb_id=request['session_id']
	#pprint(request)
	user_details_url = "https://graph.facebook.com/v2.6/%s"%fb_id
	user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':'<access_token>'}
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
