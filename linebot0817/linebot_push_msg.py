from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

def push_msg(self,event):
    if isinstance(event, MessageEvent):
                print(event)
                line_bot_api.push_message("U0a684f7f0a60d1be5dd52c93395c9c89",TextSendMessage(text="客服人員忙線中 "))
