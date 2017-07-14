<h1>Facebook-messenger-bot</h1>
<p>This is a messenger(fb) chat bot which can greet users and give the weather reports for now,But I will try to add more feautres into it.You can also make your own custom chatbot by using this project and customize the functionality as per your needs.<br/>As a beginner I Know it's tough to think that how do we make chatbots,but now a days it's really easy to make chatbots,The only thing that we have to do is "<b>Use the Resources wisely!!</b>".So follow this documentation and you can make your own working chatbots in an hour!!</p>

<!--<h3>Usefull links:-</h3><hr/>
<ul>
<li><a href="https://developers.facebook.com/docs/messenger-platform/guides/quick-start/">Facebook quickstart for building messenger chatbot</a></li>
<li><a href="https://wit.ai/docs/quickstart">Wit-Ai docs for making wit app</a></li>
<li><a href="https://github.com/wit-ai/pywit">Official wit and python intergation docs</a></li>
</ul>-->
<h2>Setup the project:-</h2><br/>
First create the virtualenv in any Location:-


```
> virtualenv chatbotenv
```

Clone this project in same location where your virtualenv exists:-

```
> git clone https://github.com/vinitraj10/Facebook-messenger-bot
```

Start the virtualenv:-

```
>chatbotenv\scripts\activate
```

Open project in virtualenv and install requirements:-

```
>cd Facebook-messenger-bot
>pip install -r requirements.txt
```
Now Go to <a href="https://wit.ai">Wit</a> and signup,create your app and follow there docs to give intents to your wit app. Or if you want my app configuration you can contact me.
So take your wit key and update in your views.py



Now go to fbchatbot>views.py:- Give some random integer value in place of <verify_token> that will be required for setting up the webhooks

```
def fbchat(request):
	if request.method == 'GET':
		if request.GET['hub.verify_token'] == <verify_token>:
			return HttpResponse(request.GET['hub.challenge'])
		else:
			return HttpResponse("Error,invalid token")

```
Download <a href="https://ngrok.com/download">Ngrok</a> for your machine after unzipping the download file you will get ngrok.exe place this exe file to your root folder and run the following commnad.

```
>python manage.py runserver
```

```
>ngrok http 8000
```

you will get some abcd.ngrok.io link for your app ,after that go to settings.py file and update ALLOWED_HOSTS:-


```
ALLOWED_HOSTS = ['abcd.ngrok.io']
```

Now follow this link to setup your webhook <a href="https://developers.facebook.com/docs/messenger-platform/guides/quick-start/">Quick start</a>
Just make sure you give your ssl certified ngrok url (https://) to callback url and verify token should be equal to that verify token which you have given in views.py file,Get your page access token and substitute it in views.py file wherever it has been used and also make sure you subscribe the app to the page According to official docs.


#USEFULL LINKS:-
<ul>
	<li><a href="https://wit.ai/docs">WIT AI DOCS</a></li>
	<li><a href="https://developers.facebook.com/docs/messenger-platform/guides/quick-start">fACEBOOK QUICK START GUIDE</a></li>
	<li><a href="https://github.com/wit-ai/pywit">wIT AI INTEGRATION WITH PYTHON APP</a></li>
</ul>

