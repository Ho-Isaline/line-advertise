# from asyncio.windows_events import None
from django.conf import settings
from linebot import LineBotApi, WebhookParser
from linebot.models import *
import boto3
from botocore.exceptions import ClientError
import datetime
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
def button(event):
    if isinstance(event, MessageEvent):
        if event.message.text == "hi":
          
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
        
    #get msg time
    def get_msg_time(self,event):
        d = datetime.datetime.fromtimestamp(event.timestamp/1000)
        msg_time = d.strftime("%Y-%m-%d %H:%M:%S.%f")
        return msg_time
    
    #auto reply
    def push_msg(self,event):    
        if isinstance(event, MessageEvent):                 
                    line_bot_api.push_message("U0a684f7f0a60d1be5dd52c93395c9c89",TextSendMessage(text="客服人員忙線中 "))

    #call dynamodb (in init)
    def log_in_dynamodb(self):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('linebot_try')
        return table
    
    #get user id
    def get_id(self,event):
        UserId = event.source.user_id
        profile = line_bot_api.get_profile(UserId)
        return profile.user_id
    
    #call the function that judge new custormer or not 
    def getmsg(self,event):
        if isinstance(event, MessageEvent): 
            userid = self.get_id(event)
            print("judge new cus or not")
            self.judge_new_customer(userid)

    #judge new custormer or not
    def judge_new_customer(self,user_id: str):
        table = self.log_in_dynamodb()
        response = table.get_item(Key={'userid': user_id,})
        try:
            response = table.put_item(    
                Item={  "userid"     :  user_id,
                        'funcId'     :  'personal',
                        'group'      :  None,
                        'groupBuying':  None,
                        'profile'    :  None,
                        'publishGB'  :  None,
                        'templateGB' :  None,
                        'record'     :  False,
                        'msgtext'  :  [ {"time":"text"} ]},
                    ConditionExpression=  "attribute_not_exists(userid)"
                )
            print("add custormer")
            
        except ClientError as err:

            # Ignore the ConditionalCheckFailedException, bubble up other exceptions.
            if err.response['Error']['Code'] != 'ConditionalCheckFailedException':
                    raise
  
    #call the record switch
    def write_in_database_ok(self,event):
        if isinstance(event, PostbackEvent):
            postback_data = event.postback.data
            if postback_data == "@customer_service":
                switch = True
                print("start to record")
                self.update_item(switch,event)
                return False
            elif postback_data == "@customer_service_off":
                switch = False
                print("stop record")
                self.update_item(switch,event)
                return False
            else:
                return True
        else:
            return True

    #record switch   
    def update_item(self,switch,event):
        table = self.log_in_dynamodb()
        response = table.update_item(
            Key={'userid': self.get_id(event)},
            UpdateExpression="set #re  = :r ",
            ExpressionAttributeNames= {'#re' : "record"} ,
            ExpressionAttributeValues={':r'  : switch},
            ReturnValues="UPDATED_NEW")
 
    #write msg into table
    def write_in_or_not(self,event):
        user_id = self.get_id(event)
        table = self.log_in_dynamodb()
        response = table.get_item(Key={'userid': user_id,})
        if response["Item"]["record"] == True:
            msgtext_history = response["Item"]["msgtext"]
            msgtext_history.append({self.get_msg_time(event):event.message.text})
            response = table.put_item(
                Item={  "userid"     :  user_id,
                        'funcId'     :  'personal',
                        'group'      :  None,
                        'groupBuying':  None,
                        'profile'    :  None,
                        'publishGB'  :  None,
                        'templateGB' :  None,
                        'record'     :  True,
                        'msgtext'  :  msgtext_history}
                )        
