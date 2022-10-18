from datetime import date
from sqlite3 import Time
from turtle import write_docstringdict
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
import datetime
import sys
sys.path.append("C:/Users/user/OneDrive/桌面/python/line-advertise/linebot0817/views.py")
from .write_in_database import write_in_database

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookParser(settings.LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


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

    
def button(event):
    if isinstance(event, MessageEvent):
        if event.message.text == "hi":
            line_bot_api.reply_message(event.reply_token,
            TemplateSendMessage(alt_text='ButtonsTemplate',
            template=ButtonsTemplate(   title='Menu',
                                        text='按下按鈕直接聯繫客服',
                                        actions=[
                                            PostbackTemplateAction(
                                            label='聯繫',
                                            data='@customer_service')])))
def button_off(event):
    if isinstance(event, MessageEvent):
        if event.message.text == "off":
            line_bot_api.reply_message(event.reply_token,
            TemplateSendMessage(
            alt_text='ButtonsTemplate',
            template=ButtonsTemplate(   title='Menu',
                                        text='結束客服',
                                        actions=[
                                            PostbackTemplateAction(
                                            label='關掉',
                                            data='@customer_service_off')])))