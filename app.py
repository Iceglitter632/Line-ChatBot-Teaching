from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('aUSuY0PjP7h0aNG292hfarEUNio+P6Ok9WIK5j8vg2ozYKVVVK7riLbOOmx9ZjS7MBk2vOcws8PxM0QmBkBdkE0rXrEJe112zBUDuYrJDCZWYV3CVnIeQR8iL4rpzGexqLDDPpRYvHoOqhfPBt4yjgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('3fa989cb8c9b1f9352154c94bb177239')

# 監聽所有來自 /callback 的 Post Request
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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if event.message.text == "文字":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))
    elif event.message.text == "貼圖":
        line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=1, sticker_id=2))
    elif event.message.text == "圖片":
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url='https://i1.kknews.cc/SIG=2ru26a9/ctp-vzntr/15301131549198023s8q5n0.jpg', preview_image_url='https://i1.kknews.cc/SIG=2ru26a9/ctp-vzntr/15301131549198023s8q5n0.jpg'))
    elif event.message.text == "影片":
        line_bot_api.reply_message(event.reply_token,VideoSendMessage(original_content_url='https://www.youtube.com/watch?v=7u4n2JyBTfU&t=28s', preview_image_url='https://i1.kknews.cc/SIG=2ru26a9/ctp-vzntr/15301131549198023s8q5n0.jpg'))
    elif event.message.text == "音訊":
        line_bot_api.reply_message(event.reply_token,AudioSendMessage(original_content_url='音訊網址', duration=100000))
    elif event.message.text == "位置":
        line_bot_api.reply_message(event.reply_token,LocationSendMessage(title='my location', address='Tainan', latitude=22.994821, longitude=120.196452))
  
    elif event.message.text == "樣板":    
        buttons_template = TemplateSendMessage(
        alt_text='目錄 template',
        template=ButtonsTemplate(
            title='Template-樣板介紹',
            text='Template分為四種，也就是以下四種：',
            thumbnail_image_url='https://i1.kknews.cc/SIG=2ru26a9/ctp-vzntr/15301131549198023s8q5n0.jpg',
            actions=[
                MessageTemplateAction(
                    label='Buttons Template',
                    text='Buttons Template'
                ),
                MessageTemplateAction(
                    label='Confirm template',
                    text='Confirm template'
                ),
                MessageTemplateAction(
                    label='Carousel template',
                    text='Carousel template'
                ),
                MessageTemplateAction(
                    label='Image Carousel',
                    text='Image Carousel'
                )
            ]
        )
    )
        line_bot_api.reply_message(event.reply_token, buttons_template)

  
    elif event.message.text == "Confirm template":
        #print("Confirm template")       
        Confirm_template = TemplateSendMessage(
        alt_text='目錄 template',
        template=ConfirmTemplate(
            title='這是ConfirmTemplate',
            text='這就是ConfirmTemplate,用於兩種按鈕選擇',
            actions=[                              
                PostbackTemplateAction(
                    label='Y',
                    text='Y',
                    data='action=buy&itemid=1'
                ),
                MessageTemplateAction(
                    label='N',
                    text='N'
                )
            ]
        )
    )
        line_bot_api.reply_message(event.reply_token,Confirm_template)
   

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
