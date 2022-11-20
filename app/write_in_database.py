from django.conf import settings
from linebot.models import *
import boto3
from botocore.exceptions import ClientError
import datetime

class write_in_database():
    
    def __init__(self,line_bot_api):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('linebot_try')
        
    #get msg time
    def get_msg_time(self,event):
        d = datetime.datetime.fromtimestamp(event.timestamp/1000)
        msg_time = d.strftime("%Y-%m-%d %H:%M:%S.%f")
        return msg_time
    


    #judge new custormer or not
    def verifyCustomer_elseCreateItem(self,user_id: str):
        res = self.table.get_item(Key={'userid': user_id,})
        try:
            res = self.table.put_item(    
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
    def record_auth(self,postback_data,user_id):
        print(postback_data, user_id)
        if postback_data == "@customer_service":
            switch = True
            print("start to record")
            self.switch_auth(switch,user_id)
            return False
        elif postback_data == "@customer_service_off":
            switch = None
            print("stop record")
            self.switch_auth(switch,user_id)
            return False
        else:
            return True

    #record switch   
    def switch_auth(self,switch,userId):
        self.table.update_item(
            Key={'userid': userId},
            UpdateExpression="set #re  = :r ",
            ExpressionAttributeNames= {'#re' : "record"} ,
            ExpressionAttributeValues={':r'  : switch},
            ReturnValues="UPDATED_NEW")
 
    #write msg into table
    def write_indb(self,event,user_id):
        response = self.table.get_item(Key={'userid': user_id,})
        if response["Item"]["record"] == True:
            msgtext_history = response["Item"]["msgtext"]
            msgtext_history.append({self.get_msg_time(event):event.message.text})
            response = self.table.put_item(
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
