from django.http import HttpResponse
from .template_message import get_hi_message, get_off_message
from .tools import LineSDK
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from .write_in_database import update_dynamodb


line = LineSDK()
handler = line.handler


def callback(request):
    if request.method == 'POST':
    # get X-Line-Signature header value
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        # get request body as text
        body = request.body.decode('utf-8')
        # handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            print("Invalid signature. Please check your channel access token/channel secret.")
            return HttpResponse(400)
        return HttpResponse('OK')
  

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "hi":
        line.send_msg(event.reply_token, get_hi_message())
        
    elif event.message.text == "off":
        line.send_msg(event.reply_token, get_off_message())
    
    else:
        db = update_dynamodb(event, "msg")
        db.judge_new_customer()
        db.updata_data()

# 1 -> get postback_data  2 -> get dynamodb info(custormor exist or not)
# 3 -> update record_auth
@handler.add(PostbackEvent)
def handle_postback(event):
    db = update_dynamodb(event, "post")
    db.judge_new_customer()
    db.record_auth()
    
    
    


































#from linebot.exceptions import InvalidSignatureError, LineBotApiError
# import datetime
#import sys
#sys.path.append("C:/Users/user/OneDrive/桌面/python/line-advertise/linebot0817/views.py")
# from linebot import LineBotApi, WebhookParser
# from django.views.decorators.csrf import csrf_exempt
# from django.http import HttpResponseBadRequest, HttpResponseForbidden
# from datetime import date
# from sqlite3 import Time
# from turtle import write_docstringdict
# from django.shortcuts import render
# from django.conf import settings



# def button(event):
#     if isinstance(event, MessageEvent):
#         if event.message.text == "hi":
#             line_bot_api.reply_message(event.reply_token,
#             TemplateSendMessage(alt_text='ButtonsTemplate',
#             template=ButtonsTemplate(   title='Menu',
#                                         text='按下按鈕直接聯繫客服',
#                                         actions=[
#                                             PostbackTemplateAction(
#                                             label='聯繫',
#                                             data='@customer_service')])))

# def button_off(event):
#     if isinstance(event, MessageEvent):
#         if event.message.text == "off":
#             line_bot_api.reply_message(event.reply_token,
#             TemplateSendMessage(
#             alt_text='ButtonsTemplate',
#             template=ButtonsTemplate(   title='Menu',
#                                         text='結束客服',
#                                         actions=[
#                                             PostbackTemplateAction(
#                                             label='關掉',
#                                             data='@customer_service_off')])))

# @csrf_exempt
# def callback(request):
#     if request.method == 'POST':
#         signature = request.META['HTTP_X_LINE_SIGNATURE']
#         body = request.body.decode('utf-8')
#         try:
#             events = parser.parse(body, signature)
#         except InvalidSignatureError:
#             return HttpResponseForbidden()
#         except LineBotApiError:
#             return HttpResponseBadRequest()
#         bot = write_in_database(line_bot_api)
#         for event in events: #因為寫入db和判斷是不是新使用者會需要一點時間，所以如果遇到使用者迅速地傳多封信息的時候，events會不只一個事件
#             button(event)
#             button_off(event)
#             bot.write_in_database_ok(event)
#             bot.getmsg(event)
#             if not isinstance(event, PostbackEvent):
#                 bot.write_in_or_not(event)
#         return HttpResponse()
#     else:
#         return HttpResponseBadRequest()