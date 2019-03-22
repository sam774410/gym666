# encoding: utf-8
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,VideoSendMessage,
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
from datetime import datetime,timezone,timedelta


def main_info(gym_name, gym_now, gym_total, swim_now, swim_total, tmp):

    dt = datetime.utcnow()
    dt = dt.replace(tzinfo=timezone.utc)
    tzutc_8 = timezone(timedelta(hours=8))
    local_dt = dt.astimezone(tzutc_8)
    #print(local_dt)
    #print(local_dt.strftime('%Y-%m-%d %H:%M'))
  
    mdatetime = local_dt.strftime('%Y-%m-%d %H:%M')

    bubble = BubbleContainer(
        direction='ltr',
        body = BoxComponent(
            layout = 'vertical',
            contents = [
                TextComponent(text='即時人流資訊', weight='bold', size='sm', color='#1DB446'),
                TextComponent(text=gym_name, weight='bold', size='xxl', margin='md'),
                TextComponent(text=tmp, size='xs', color='#aaaaaa', margin='sm', wrap=True),
                SeparatorComponent(margin='xxl'),
        

        BoxComponent(
            layout = 'horizontal',
            margin = 'xxl',
            spacing = 'sm',
            contents = [
                
                #picture
                BoxComponent(
                    layout = 'vertical',
                    flex = 0,
                    contents = [
                        ImageComponent(url='https://i.imgur.com/3qQCq1f.png', size = 'sm', aspectRatio="16:9", aspectMode="fit"),
                        ImageComponent(url='https://i.imgur.com/B37vhyK.png', size = 'sm', aspectRatio="16:9", aspectMode="fit", margin = 'lg')
                    ]
                ),

                #info
                BoxComponent(
                    layout = 'vertical',
                    align = 'center',
                    flex = 1,
                    contents = [
                        TextComponent(text='   現在人數: {0} 人'.format(gym_now), flex=2, size='lg', weight='bold', color='#1DB446', gravity='center'),
                        
                        TextComponent(text='   容留: {0} 人'.format(gym_total), flex=1, size='md', gravity='center'),

                        TextComponent(text='   現在人數: {0} 人'.format(swim_now), flex=2, size='lg', weight='bold', color='#1DB446', gravity='center', margin='xl'),
                        
                        TextComponent(text='   容留: {0} 人'.format(swim_total), flex=1, size='md', gravity='center')
                    ]
                )    
            ]
        ),
                SeparatorComponent(margin='lg'),
            ]
        ),

        footer=BoxComponent(
            layout='horizontal',
            margin='md',
            spacing='md',
            contents=[
                TextComponent(text="查詢時間", size="xs", color="#aaaaaa", flex=0),
                TextComponent(text=mdatetime, size="xs", color="#aaaaaa", align="end")
            ]
        )
    )
    message = FlexSendMessage(alt_text="即時人流資訊", contents=bubble)
    return message