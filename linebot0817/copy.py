from asyncio.windows_events import NULL
from ctypes.wintypes import BOOL
from datetime import date
from pickle import FALSE
from re import L
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
import boto3
from botocore.exceptions import ClientError
import datetime
from boto3.dynamodb.conditions import Key
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

def button(event):
    if isinstance(event, MessageEvent):
        if event.message.text == "hi":
            print("11")
            line_bot_api.reply_message(  # 回復傳入的訊息文字
            event.reply_token,
            TemplateSendMessage(
    alt_text='ButtonsTemplate',
    template=ButtonsTemplate(
                            title='Menu',
                            text='按下按鈕直接聯繫客服',
                            actions=[
                                PostbackTemplateAction(
                                    label='聯繫',
                                    text='聯繫',
                                    data='@customer_service'
                                    )
                                    ]
                            )
                                )
                                        )

def button_off(event):
    if isinstance(event, MessageEvent):
        if event.message.text == "off":
            print("11")
            line_bot_api.reply_message(  # 回復傳入的訊息文字
            event.reply_token,
            TemplateSendMessage(
    alt_text='ButtonsTemplate',
    template=ButtonsTemplate(
                            title='Menu',
                            text='結束客服',
                            actions=[
                                PostbackTemplateAction(
                                    label='聯繫',
                                    text='聯繫',
                                    data='@customer_service_off'
                                    )
                                    ]
                            )
                                )
                                        )

class write_in_database():
    
    def __init__(self,line_bot_api):
        
        self.__line_bot_api = line_bot_api
        
    '''下面這段是紀錄時間(event)'''
    def get_msg_time(self,event):
        d = datetime.datetime.fromtimestamp(event.timestamp/1000)
        msg_time = d.strftime("%Y-%m-%d %H:%M:%S.%f")
        print(msg_time)
        return msg_time
    
    '''下面這段是非上班時間自動回復'''
    def push_msg(self,event):
        
        if isinstance(event, MessageEvent):
                    
                    print(event)
                    
                    line_bot_api.push_message("U0a684f7f0a60d1be5dd52c93395c9c89",TextSendMessage(text="客服人員忙線中 "))

    
    '''下面這段是登入dynamodb'''
    def log_in_dynamodb(self):

        dynamodb = boto3.resource('dynamodb')

        table = dynamodb.Table('linebot_try')

        return table
    
    
    '''取user_id'''
    def get_id(self,event):
        
        UserId = event.source.user_id
        
        profile = line_bot_api.get_profile(UserId)

        return profile.user_id
    
    '''收到訊息之後接判斷是否新用戶'''
    def getmsg(self,event):
        if isinstance(event, MessageEvent):
            userid = self.get_id(event)
            print("judge new cus or not")
            self.judge_new_customer(userid,event)

    '''下面這段是判斷是否新用戶'''
    def judge_new_customer(self,user_id: str,event):

        table = self.log_in_dynamodb()
        response = table.get_item(Key={'userid': user_id,})
        try:
            response = table.put_item(
                Item={  "userid"     :  user_id,
                        'funcId'     :  'personal',
                        'group'      :  NULL,
                        'groupBuying':  NULL,
                        'profile'    :  NULL,
                        'publishGB'  :  NULL,
                        'templateGB' :  NULL,
                        'record'     :  False,
                        'msgtext'  :  [] },
                    ConditionExpression=  "attribute_not_exists(userid)"
                )
            print("not add custormer")
            
        except ClientError as err:
            print(f'[LineSDK/add_user] {err}')
            # Ignore the ConditionalCheckFailedException, bubble up other exceptions.
            if err.response['Error']['Code'] != 'ConditionalCheckFailedException':
                    raise

        
    '''客服人員開關'''
    def write_in_database_ok(self,event):
        if isinstance(event, PostbackEvent):
            postback_data = event.postback.data
            if postback_data == "@customer_service":

                switch = True

                print("開啟")

                self.update_item(switch,event)

                return False

            elif postback_data == "@customer_service_off":
                
                switch = False
            
                print("關掉")
            
                self.update_item(switch,event)

                return False
            else:
                return True
        else:
            return True
          


    def update_item(self,switch,event):

        table = self.log_in_dynamodb()
        print("開關執行")
        
        response = table.update_item(
            Key={'userid': self.get_id(event)},
            UpdateExpression="set #re  = :r ",
            ExpressionAttributeNames= {'#re' : "record"} ,
            ExpressionAttributeValues={':r'  : switch},
            ReturnValues="UPDATED_NEW")
       
        print(response)
 
 
    '''判斷是否寫入'''

    def write_in_or_not(self,event):

        user_id = self.get_id(event)
        table = self.log_in_dynamodb()
        response = table.get_item(Key={'userid': user_id,})
        print("對")
        
        if response["Item"]["record"] == True:
            print("你好")
            time_key = self.get_msg_time(event)
            
            msg_text  = event.message.text
            print(msg_text)
            print(time_key)
            response = table.update_item(
            Key={'userid': user_id},
            UpdateExpression="SET #msg = list_append( #msg, :t) ",
            ExpressionAttributeNames= {'#msg' : "msgtext"} ,
            ExpressionAttributeValues={':t' : [ time_key,msg_text] },
            ReturnValues="UPDATED_NEW")
            print("record",time_key,msg_text)


 

