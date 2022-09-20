from django.shortcuts import render
from .forms import MyForm
from linebot import LineBotApi
from linebot.models import TextSendMessage
from flask import Flask
from linebot import LineBotApi, WebhookHandler
from linebot.models import *
from django.conf import settings
import boto3
from .models import Id_Name_dict
import json

app = Flask(__name__)

line_bot_api = LineBotApi("1ob3ZSFOu0arzAXk8xh7EnR0x+hOOlJ5p7L603loiIoYP6p0sK1HM+AePqF+pHXEqjTM2PDnXlwN4R3typt1MZHE12JC6n5WLibbMHOA+z7YVp1qQ8sDI2zcn8LcVfEr6APdOhrthUDb13MYGTIyUVGUYhWQfeY8sLGRXgo3xvw=")
handler = WebhookHandler("04c9dfd04fc0dafebbc4cb32c6e6fd5f")




def home(request):
	return render(request, 'home.html')


def entry(request):
	form = MyForm(request.POST or None)
	if request.method == 'POST':
		form = MyForm(request.POST)
		if form.is_valid():
			response = request.POST
			context = response['context']
			username = form.cleaned_data.get('user')
			print(context, username)
			try:
				message = json.loads(context)
				line_bot_api.multicast(username,FlexSendMessage(alt_text='advertise', contents = message))
			except ValueError:
				line_bot_api.multicast(username,TextSendMessage(text = context))
			
	form = MyForm()
	return render(request, 'entry.html', {'form': MyForm()})
	
	




