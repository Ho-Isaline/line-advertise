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
handler = WebhookHandler("3b4bc5fb33633b211c2e19d4f37b9ef5")




def home(request):
	return render(request, 'home.html')


def entry(request):
	form = MyForm(request.POST or None)
	if request.method == 'POST':
		form = MyForm(request.POST)
		if form.is_valid():
			response = request.POST
			print('form response: ', response)
			context1 =  response['context1']
			context2 = response['context2']
			context3 = response['context3']
			contexts_elements = [context1,context2,context3]
			print('contexts: ', contexts_elements)
			username = form.cleaned_data.get('user')
			print('username: ', username)
			contexts = []
			
			for context in contexts_elements:
				if isinstance(context,str):
					contexts.append(TextSendMessage(text = context))
				elif isinstance(context,None):
					pass
				else:
					print('in except')
					message = json.loads(context)
					contexts.append(FlexSendMessage(alt_text='advertise', contents = message))

			print('contexts: ', contexts)
			line_bot_api.multicast(username,contexts)
			
	form = MyForm()
	return render(request, 'entry.html', {'form': MyForm()})
	
	




