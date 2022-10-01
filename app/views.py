from ast import Expression
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
from boto3.dynamodb.conditions import Attr

app = Flask(__name__)

line_bot_api = LineBotApi(
    "1ob3ZSFOu0arzAXk8xh7EnR0x+hOOlJ5p7L603loiIoYP6p0sK1HM+AePqF+pHXEqjTM2PDnXlwN4R3typt1MZHE12JC6n5WLibbMHOA+z7YVp1qQ8sDI2zcn8LcVfEr6APdOhrthUDb13MYGTIyUVGUYhWQfeY8sLGRXgo3xvw=")
handler = WebhookHandler("04c9dfd04fc0dafebbc4cb32c6e6fd5f")


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
					contexts.append(FlexSendMessage(alt_text='advertise', contents=message))
			line_bot_api.multicast(username, contexts)
	form = MyForm()
	return render(request, 'entry.html', {'form': MyForm()})


def group(request):
	form = CreateGroupForm(request.POST or None)
	if request.method == 'POST':
		form = CreateGroupForm(request.POST)
		if form.is_valid():
			response = request.POST
			users = form.cleaned_data.get('user')
			groupName = form.cleaned_data.get('groupName')
			DYNAMO_ENDPOINT = getattr(settings, 'DB_ENDPOINT', None)
			dynamodb = boto3.resource(
			    'dynamodb', region_name='us-east-1', endpoint_url=DYNAMO_ENDPOINT)
			view_table = dynamodb.Table('LineService')
			print(users)
			
			
			
			for userId in users:
				resp = view_table.get_item(Key={'userId': userId, 'funcId': 'personal'})['Item']
				print(resp.keys())
				if 'group'  in resp.keys():
					print('have group attribute')
					view_table.update_item(
						Key={'userId': userId, 'funcId': 'personal'},
						UpdateExpression = "SET #group = list_append(#group, :S)",
						ExpressionAttributeNames = {'#group' : 'group'},
						ExpressionAttributeValues = {':S' : groupName },
						ReturnValues = 'UPDATED_NEW'
					)
					
					
				else:
					print('no group attribute')
					view_table.update_item(
						Key={'userId': userId, 'funcId': 'personal'},
						UpdateExpression = "SET #group = :l",
						ExpressionAttributeNames = {'#group' : 'group'},
						ExpressionAttributeValues = {':l' : [groupName] },
						ReturnValues = 'UPDATED_NEW'
					)
				
					
	form = CreateGroupForm()
	return render(request, 'group.html', {'form': CreateGroupForm()})