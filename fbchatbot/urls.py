from django.conf.urls import url
from fbchatbot import views
urlpatterns = [
	
	url(r'^$',views.fbchat,name="fbchat"),


]