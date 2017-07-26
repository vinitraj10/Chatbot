import json,requests,datetime
from pprint import pprint
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
	pprint(result)
	temp_max=int(((result['daily']['data'][0]['temperatureMax'])-32)*0.5555555555555556)
	temp_min=int(((result['daily']['data'][0]['temperatureMin'])-32)*0.5555555555555556)
	#sunrise=datetime.datetime.fromtimestamp(int(result['daily']['data'][0]['sunriseTime'])).strftime('%H:%M:%S')
	#sunset=datetime.datetime.fromtimestamp(int(result['daily']['data'][0]['sunsetTime'])).strftime('%H:%M:%S')
	#timeZone=(result['timezone'])
	summary=result['hourly']['summary']
	final_report="Max temp : " + str(temp_max) + " °C \n" + "Min temp : " + str(temp_min) + " ° C \n" + "Summary : " + str(summary)
	post_weather_fb(final_report,fb_id)

def cleaning_text(text):
	fresh_text=[]
	for i in range(2,len(text)-1):
		fresh_text.append(text[i])
	fresh_text = "".join(fresh_text)
	return fresh_text