from linebot.models import *
import boto3
from botocore.exceptions import ClientError
from .tools import get_line_info


class update_dynamodb():
    def __init__(self, event, switch:str):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('linebot_try')
        info = get_line_info(event)
        self.user_id = info.get_user_id()
        if switch == "post":
            self.data = info.get_postback_data()
        else:
            self.msg = info.get_msg()
        
    #judge new custormer or not
    def judge_new_customer(self):
        self.table.get_item(Key={'userid': self.user_id})
        # custormer not exist
        try:
            self.table.put_item(    
                Item={  "userid"     :  self.user_id,
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
        # custormer exist
        except ClientError as err:
            # Ignore the ConditionalCheckFailedException, bubble up other exceptions.
            if err.response['Error']['Code'] != 'ConditionalCheckFailedException':
                raise
  
    #call the record switch
    def record_auth(self):
        if self.data == "@customer_service":
            switch = True
            print("start to record")
            self.switch_auth(switch)
            return False
        elif self.data == "@customer_service_off":
            switch = None
            print("stop record")
            self.switch_auth(switch)
            return False
        else:
            return True

    #record switch   
    def switch_auth(self,switch):
        self.table.update_item(
            Key={'userid': self.user_id},
            UpdateExpression="set #re  = :r ",
            ExpressionAttributeNames= {'#re' : "record"} ,
            ExpressionAttributeValues={':r'  : switch},
            ReturnValues="UPDATED_NEW")
 
    #write msg into table
    def updata_data(self):
        response = self.table.get_item(Key={'userid': self.user_id})
        try:
            if response["Item"]["record"] == True:
                msgtext_history = response["Item"]["msgtext"]
                msgtext_history.append(self.msg)
                response = self.table.put_item(
                    Item={  "userid"     :  self.user_id,
                            'funcId'     :  'personal',
                            'group'      :  None,
                            'groupBuying':  None,
                            'profile'    :  None,
                            'publishGB'  :  None,
                            'templateGB' :  None,
                            'record'     :  True,
                            'msgtext'  :  msgtext_history}
                    )        
        except KeyError:
            print("未加好友無紀錄")
            pass





# from django.conf import settings
# from linebot import LineBotApi, WebhookParser
# import datetime
# line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
# parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
# self.__line_bot_api = line_bot_api
        
    # #get msg time
    # def get_msg_time(self,event):
    #     d = datetime.datetime.fromtimestamp(event.timestamp/1000)
    #     msg_time = d.strftime("%Y-%m-%d %H:%M:%S.%f")
    #     return msg_time
    
    # #get user id
    # def get_id(self,event):
    #     UserId = event.source.user_id
    #     profile = line_bot_api.get_profile(UserId)
    #     return profile.user_id
    
    # #call the function that judge new custormer or not 
    # def getmsg(self,event):
    #     if isinstance(event, MessageEvent): 
    #         userid = self.get_id(event)
    #         print("judge new cus or not")
    #         self.judge_new_customer(userid)