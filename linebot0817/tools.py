from linebot import LineBotApi, WebhookHandler
from django.conf import settings
import datetime
from linebot.exceptions import LineBotApiError


class LineSDK():
    def __init__(self):
        self.line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
        self.handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)

    def send_msg(self, reply_token:str, reply_event):
        self.line_bot_api.reply_message(
            reply_token, reply_event
        )
        
    def get_profile_detail(self, user_id:str):
         try:
             return self.line_bot_api.get_profile(user_id)
         except LineBotApiError as err:
             print(f'[LineSDK/get_profile_detail] UserID {user_id} failed to request account detail because of {err}.')

        
        
class get_line_info():
    def __init__(self, event):
        self.event = event

    def get_msg(self):
        date = datetime.datetime.fromtimestamp(self.event.timestamp/1000)
        return {date.strftime("%Y-%m-%d %H:%M:%S.%f"):self.event.message.text}
    
    def get_user_id(self):
        return self.event.source.user_id
    
    def get_postback_data(self):
        return self.event.postback.data
