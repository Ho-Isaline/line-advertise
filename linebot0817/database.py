from asyncio.windows_events import NULL
import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('linebot_try')
user_id = "apple"
msg_time = 0
msg_text = 0
table.put_item(
Item={"userid"     :  user_id,
      'funcId'     :  'personal',
      'group'      :  None,
      'groupBuying':  None,
      'profile'    :  None,
      'publishGB'  :  None,
      'templateGB' :  None,
      'record'     :  {
        'switch': False,
        'text'  : {
            'msg': { msg_time , msg_text}
        }
      }
})
print(table)

