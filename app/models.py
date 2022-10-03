from django.conf import settings
from boto3.dynamodb.conditions import Attr
import boto3

class ConnectDatabase:
    #get table
    def __init__(self, tablename:str):
        #dynamodb configure has been set and tablename is a parament
        dynamodb = boto3.resource('dynamodb')
        self.view_table = dynamodb.Table(tablename)
    
    #get user list    
    def scan_table(self, key:str, select_key:str, object:str, item1:str, item2:str):
        #key -> Partition key name or sort key name(column name)
        #select_key -> the attribute value you select(to sieve the object out by key's attribute)
        #object -> where data is(column name)
        #two items only 
        
        #for example:
        #   scan_table('funcId', 'personal', 'profile', "userId", "displayName")
        
        GROUP_CHOICES_DB = self.view_table.scan(
            FilterExpression=Attr(key).eq(select_key),
            Select = 'SPECIFIC_ATTRIBUTES',
            ProjectionExpression=object
        )
        USER_LIST = []
        items = GROUP_CHOICES_DB['Items']
        for item in items:
            userId = item[object][item1]
            userName = item[object][item2]
            USER_LIST.append((userId, userName))
        return USER_LIST
    
    #get where the attribute is
    def item_place(self, partition_key, partition_value, sort_key, sort_value='personal'):
        global resp
        resp = self.view_table.get_item(Key={partition_key : partition_value, sort_key : sort_value})['Item']
        return resp
    
    #add group attribute
    def add_item(self, partition_key, partition_value, sort_key, sort_value, attr:str, attrname):
        if attrname in resp[attr]:
            pass
        else:
            self.view_table.update_item(
                Key={partition_key : partition_value, sort_key : sort_value},
                UpdateExpression = "SET #group = list_append(#group, :l)",
                ExpressionAttributeNames = {'#group' : attr},
                ExpressionAttributeValues = {':l' : [attrname] },
                ReturnValues = 'UPDATED_NEW'
            )
                
    def set_item(self, partition_key, partition_value, sort_key, sort_value, attr:str, attrname):
        self.view_table.update_item(
            Key={partition_key : partition_value, sort_key : sort_value},
            UpdateExpression = "SET #group = :l",
            ExpressionAttributeNames = {'#group' : attr},
            ExpressionAttributeValues = {':l' : [attrname] },
            ReturnValues = 'UPDATED_NEW'		
        )
    

table = ConnectDatabase('LineService')
USER_LIST = table.scan_table('funcId', 'personal', 'profile', "userId", "displayName")






#from collections import UserList
#from select import select
#from dynamorm import DynaModel
#from marshmallow import fields

# '''
# while 'LastEvaluatedKey' in GROUP_CHOICES_DB:
#     response = view_table.scan(
#         ExclusiveStartKey=response['LastEvaluatedKey'],
#     )
#     data.extend(response['Items'])
# print('table_total_len', len(data))
# for dict in data:
#     func = dict.get('funcId')
#     if func == 'personal':
#         GROUP_CHOICES.append((dict.get('userId'), dict.get('userId')))
# '''

# class MyTable(DynaModel):
#     	class Table:
# 		resource_kwargs = {'endpoint_url': settings.DB_ENDPOINT}
# 		name = settings.DB_TABLE
# 		hash_key = 'user'
# 		read = 25
# 		write = 5

# 	class Schema:
# 		user = fields.String(required=True)
# 		context = fields.String(required=True)