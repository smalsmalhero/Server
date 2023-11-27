#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from urllib.parse import urlparse

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('AU/QDri2KE1NXmPy3qxcO7hY9+GmviLxov3guTlLUT5XfpsrRlXA7we4I32aRebmsHxr/MMl6ywNJLHSD/qmBRvYmFt0esCWnAFiGkYaijl9D05w1eB3+lgscrfxpe8WLtKF3kdoYQCY5dObj0aTXwdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('9cf048df757b3f7caabf30a89c853c9a')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['GET','POST'])
def callback():
  line_bot_api.push_message('U3f07def73305496dc2076532560edcbc', TextSendMessage(text='你可以開始了'))
  try:
    u = urlparse("https://server-slr7.onrender.com/callbcak?msg=1)
    if u.query == 'msg=1':
      line_bot_api.push_message('U3f07def73305496dc2076532560edcbc', TextSendMessage(text='早安 吃藥時間到囉! ฅ●ω●ฅ'))
    elif u.query == 'msg=1':
      # 如果 msg 等於 2，發送午安
      line_bot_api.push_message('U3f07def73305496dc2076532560edcbc', TextSendMessage(text='午安 吃藥時間到囉!(๑´ㅂ`๑) '))
    elif u.query == 'msg=1':
      # 如果 msg 等於 3，發送晚安
      line_bot_api.push_message('U3f07def73305496dc2076532560edcbc', TextSendMessage(text='早安 吃藥時間到囉! ٩(｡・ω・｡)و'))
    else:
      msg = 'ok'   # 如果沒有 msg 或 msg 不是 1～4，將 msg 設定為 ok
    return msg
  except:
    print('error')

 
#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token,message)

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
