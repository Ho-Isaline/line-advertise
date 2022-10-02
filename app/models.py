from select import select
from dynamorm import DynaModel
from marshmallow import fields
from django.conf import settings
from boto3.dynamodb.conditions import Attr
import boto3

'''
class MyTable(DynaModel):
	class Table:
		resource_kwargs = {'endpoint_url': settings.DB_ENDPOINT}
		name = settings.DB_TABLE
		hash_key = 'user'
		read = 25
		write = 5

	class Schema:
		user = fields.String(required=True)
		context = fields.String(required=True)

'''

DYNAMO_ENDPOINT = getattr(settings, 'DB_ENDPOINT', None)
dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url=DYNAMO_ENDPOINT)
view_table = dynamodb.Table('LineService')
        
GROUP_CHOICES_DB = view_table.scan(
	FilterExpression=Attr('funcId').eq('personal'),
	Select = 'SPECIFIC_ATTRIBUTES',
    ProjectionExpression='profile'
)


CHOICES = []
Id_Name_dict = {}
items = GROUP_CHOICES_DB['Items']

for item in items:
    userId = item['profile']['userId']
    userName = item['profile']['displayName']
    CHOICES.append((userId, userName))

USER_LIST = CHOICES

'''
while 'LastEvaluatedKey' in GROUP_CHOICES_DB:
    response = view_table.scan(
        ExclusiveStartKey=response['LastEvaluatedKey'],
    )
    data.extend(response['Items'])
print('table_total_len', len(data))
for dict in data:
    func = dict.get('funcId')
    if func == 'personal':
        GROUP_CHOICES.append((dict.get('userId'), dict.get('userId')))
'''
