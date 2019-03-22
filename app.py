# encoding: utf-8
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,VideoSendMessage,ImageSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton
)


from template.dashboard import main_info
from datasource.current_people import A_site, B_site, C_site, Other_site, current_people
from datasource.location_query import gym_search, gym_detail, gym_address
from dialogflow.nlp import get_GYM_NAME
from helper.config import line_channel_secret, line_channel_access_token

app = Flask(__name__)

handler = WebhookHandler(line_channel_secret) 
line_bot_api = LineBotApi(line_channel_access_token) 


USER_ID=''
USER_NAME=''

@app.route('/')
def index():
    return "<p>Hello gym bot!</p>"

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
        abort(400)

    return 'OK'

# ================= 機器人區塊 Start =================
@handler.add(MessageEvent, message=TextMessage)  # default
def handle_text_message(event):     
    
    if isinstance(event.source, SourceUser) or isinstance(event.source, SourceGroup) or isinstance(event.source, SourceRoom):
        profile = line_bot_api.get_profile(event.source.user_id)
        USER_ID = profile.user_id
        USER_NAME = profile.display_name

    msg = event.message.text #message from user

    #Dialogflow
    response = get_GYM_NAME(msg)

    if bool(response["isOk"]):
        
        line_single_push(USER_ID, response["response"])
        
        result = current_people(response["gymName"])
        address = gym_address(response["gymName"])
        #line_single_push(USER_ID, str(result))

        #push info ... flex msg...
        tmplate = main_info(response["gymName"], result[0], result[1], result[2], result[3], address)
        line_bot_api.reply_message(
            event.reply_token, tmplate)

    elif bool(response["isOk"]) is False:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response["response"]))


@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):

    if isinstance(event.source, SourceUser) or isinstance(event.source, SourceGroup) or isinstance(event.source, SourceRoom):
        profile = line_bot_api.get_profile(event.source.user_id)
        USER_ID = profile.user_id
        USER_NAME = profile.display_name

    longitude = str(event.message.longitude)
    latitude = str(event.message.latitude)
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     LocationSendMessage(
    #         title=event.message.title, address=event.message.address,
    #         latitude=event.message.latitude, longitude=event.message.longitude
    #     )
    # )
    #line_single_push(USER_ID, str(event.message.longitude))
    

    line_single_push(USER_ID, '查詢中 請稍候...')   
    res = gym_search(longitude, latitude)

    if bool(res["isOk"]):
        res = res["response"]

        #web url
        '''web_res = []
        for i in range(0, 3):
            result = gym_detail(res[i]['GymID'])
            web_res.append(result["web"])'''

        carousel_template = CarouselTemplate(columns=[
                CarouselColumn(thumbnail_image_url=res[0]['Photo1'],text='約 '+str(res[0]['Distance'])+' 公里', title=res[0]['Name'], actions=[
                    MessageAction(label='查詢即時資訊', text=res[0]['Name'])
                    #URIAction(label='官方網站', uri=web_res[0])
                ]),
                CarouselColumn(thumbnail_image_url=res[1]['Photo1'],text='約 '+str(res[1]['Distance'])+' 公里', title=res[1]['Name'], actions=[
                    MessageAction(label='查詢即時資訊', text=res[1]['Name'])
                    #URIAction(label='官方網站', uri=web_res[1])
                ]),
                CarouselColumn(thumbnail_image_url=res[2]['Photo1'],text='約 '+str(res[2]['Distance'])+' 公里', title=res[2]['Name'], actions=[
                    MessageAction(label='查詢即時資訊', text=res[2]['Name'])
                    #URIAction(label='官方網站', uri=web_res[2])
                ])
            ])
        template_message = TemplateSendMessage(
                alt_text='附近的運動中心', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='附近暫無運動中心'))

'''    if msg in A_site.keys() or msg in B_site.keys() or msg in C_site.keys() or msg in Other_site.keys():
        res = current_people(msg)
        if res is not False:
            res = list(res)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=str(res)))

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="可以說出運動中心名稱喔～"))'''

@handler.add(PostbackEvent)
def handle_postback(event):

  '''  msg = event.postback.data
    print(msg)
    if msg in A_site.keys() or msg in B_site.keys() or msg in C_site.keys() or msg in Other_site.keys():
        res = current_people(msg)
        if res is not False:
            res = list(res)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=str(res)))
    else:
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=msg+' 暫無提供即時資訊!'))'''
    # 針對使用者各種訊息的回覆 End =========

# ================= 機器人區塊 End =================

#push text
def line_single_push(id, txt):
    line_bot_api.push_message(id, 
        TextSendMessage(text=txt))

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
    #app.run(host='0.0.0.0',port=3000)



