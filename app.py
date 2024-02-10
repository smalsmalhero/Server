#載入LineBot所需要的套件
from flask import Flask, request, abort, json
from flask_ngrok import run_with_ngrok

import openpyxl
from openpyxl import load_workbook

import requests

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

access_token = 'h3GpmGFSXkxTCCsyRziMsWA6+3eCF1o5j9WSZ8os5UEDf7LqN+YqXlQFsHPdSTwijVmGMc29uutTLHuqAf28sXtFYI5VvS74M4b24bsXQaZ80fqpb0+NH65vw3ZUcrPuMqoOHWjRBDg3JCcW/dVchgdB04t89/1O/w1cDnyilFU='
channel_secret = '7befd1a844f9ea937873cd2729b04859'
# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi(access_token)
# 必須放上自己的Channel Secret
handler = WebhookHandler(channel_secret)

# LINE push 訊息函式
def push_message(msg, uid, token):
    headers = {'Authorization':f'Bearer {token}','Content-Type':'application/json'}   
    body = {
    'to':uid,
    'messages':[{
            "type": "text",
            "text": msg
        }]
    }
    req = requests.request('POST', 'https://api.line.me/v2/bot/message/push', headers=headers,data=json.dumps(body).encode('utf-8'))
    print(req.text)

# LINE 回傳訊息函式
def reply_message(msg, rk, token):
    headers = {'Authorization':f'Bearer {token}','Content-Type':'application/json'}
    body = {
    'replyToken':rk,
    'messages':[{
            "type": "text",
            "text": msg
        }]
    }
    req = requests.request('POST', 'https://api.line.me/v2/bot/message/reply', headers=headers,data=json.dumps(body).encode('utf-8'))
    print(req.text)

# LINE 回傳圖片函式
def reply_image(msg, rk, token):
    headers = {'Authorization':f'Bearer {token}','Content-Type':'application/json'}
    body = {
    'replyToken':rk,
    'messages':[{
          'type': 'image',
          'originalContentUrl': msg,
          'previewImageUrl': msg
        }]
    }
    req = requests.request('POST', 'https://api.line.me/v2/bot/message/reply', headers=headers,data=json.dumps(body).encode('utf-8'))
    print(req.text)

# 儲存user_id資料
def write_user (user_id):
    wb = openpyxl.load_workbook('user_id.xlsx', data_only=True)    # 打開檔案
    s1 = wb['工作表1']                                              # 開啟工作表 1

    number = 1
    while(1):
        if s1[f'A{number}'].value is None:
            s1[f'A{number}'].value = user_id
            break
        elif s1[f'A{number}'].value == user_id:
            break
        else:
            number += 1
    
    wb.save('user_id.xlsx')

# 取得user_id資料
def read_user (number):
    wb = openpyxl.load_workbook('user_id.xlsx', data_only=True)  # 設定 data_only=True 只讀取計算後的數值

    s1 = wb['工作表1']
    read_data = s1[f'A{number}'].value

    return read_data


# 監聽所有來自 / 的 Post Request
@app.route("/", methods=['POST','GET'])
def linebot():
    body = request.get_data(as_text=True)
    try:
        msg = request.args.get('msg')
        number = 1
        if msg == '1':
            # 發送所有儲存的資料
            while(1):
                if read_user(number) is None:
                    break
                else:
                    # 如果 msg 等於 1，發送早安
                    push_message('早安 吃藥時間到囉! ฅ●ω●ฅ', uid=f'{read_user(number)}', token=access_token)
                    number += 1
        elif msg == '2':
            # 發送所有儲存的資料
            while(1):
                if read_user(number) is None:
                    break
                else:
                    # 如果 msg 等於 2，發送午安
                    push_message('午安 吃藥時間到囉!(๑´ㅂ`๑) ', uid=rf'{read_user(number)}', token=access_token)
                    number += 1
        elif msg == '3':
            # 發送所有儲存的資料
            while(1):
                if read_user(number) is None:
                    break
                else:
                    # 如果 msg 等於 3，發送晚安
                    push_message('晚安 吃藥時間到囉! ٩(｡・ω・｡)و', uid=f'{read_user(number)}', token=access_token)
                    number += 1
        elif msg == "4":
            # 發送所有儲存的資料
            while(1):
                if read_user(number) is None:
                    break
                else:
                    # 如果 msg 等於 4，發送睡前
                    push_message('睡覺前 也該吃藥囉! (⁠⁠ꈍ⁠ᴗ⁠ꈍ⁠)', uid=f'{read_user(number)}', token=access_token)
                    number += 1
        else:
            # 如果沒有 msg 或 msg 不是 1～4，將 msg 設定為 ok
            msg = 'ok'   
            print('成功')
        print('成功')

        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        json_data = json.loads(body)
        reply_token = json_data['events'][0]['replyToken']
        user_id = json_data['events'][0]['source']['userId']
        print(json_data)
        if 'message' in json_data['events'][0]:
            if json_data['events'][0]['message']['type'] == 'text':
                text = json_data['events'][0]['message']['text'].lower()
                if text == '設定：id' or text == '設定:id':
                    write_user(user_id)
                    reply_message('設定完成', reply_token, access_token)
        print('成功')
    except:
        print('error')
    return 'OK'
    
#主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)
