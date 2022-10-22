from linebot.models import *

def get_hi_message():
    return TemplateSendMessage(
        alt_text='ButtonsTemplate',
        template=ButtonsTemplate(
            title='Menu',
            text='按下按鈕直接聯繫客服',
            actions=[
                PostbackTemplateAction(
                label='聯繫',
                data='@customer_service')]))
    

def get_off_message():
    return TemplateSendMessage(
        alt_text='ButtonsTemplate',
        template=ButtonsTemplate(
            title='Menu',
            text='結束客服',
            actions=[
                PostbackTemplateAction(
                label='關掉',
                data='@customer_service_off')]))    