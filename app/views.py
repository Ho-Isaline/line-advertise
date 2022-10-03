from django.shortcuts import render
from .forms import CreateGroupForm, MyForm
from linebot import LineBotApi
from linebot.models import TextSendMessage
from flask import Flask
from linebot import LineBotApi, WebhookHandler
from linebot.models import *
import json
import boto3
from django.conf import settings
from .models import table


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
			username = form.cleaned_data.get('user')
			key_list = list(response.keys())
			contexts = []
			for contest_name in key_list[2::]:
				msg = response[contest_name]
				if isinstance(msg, str):
					contexts.append(TextSendMessage(text=msg))
				else:
					message = json.loads(msg)
					contexts.append(FlexSendMessage(alt_text='advertise', contents = message))
			print(contexts)
			line_bot_api.multicast(username,contexts)
				
	form = MyForm()
	return render(request, 'entry.html', {'form': MyForm()})


def group(request):
	form = CreateGroupForm(request.POST or None)
	if request.method == 'POST':
		form = CreateGroupForm(request.POST)
		if form.is_valid():
			users = form.cleaned_data.get('user')
			groupName = form.cleaned_data.get('groupName')
			for userId in users:
				resp = table.item_place('userId', userId, 'funcId')
				print(resp.keys()) #confirm that if they have the group attribute
				if 'group'  in resp.keys():
					table.add_item('userId', userId, 'funcId', 'personal', 'group', groupName)	
				else:
					print('no group attribute')
					table.set_item('userId', userId, 'funcId', 'personal', 'group', groupName)			
	form = CreateGroupForm()
	return render(request, 'group.html', {'form': CreateGroupForm()})