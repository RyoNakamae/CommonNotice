# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# 3系前提
# ---------------------------------------------------------------------------


import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import requests
import json

# 送信元のメアドと名前、パスワード（Gmailの場合はアプリパスワードを発行し使用する）
FROM_ADDRESS = 'xxxxx@gmail.com'
FROM_NAME = 'XXXXXX'
MY_PASSWORD = 'xxxxx'

# 送信先はリスト型にしておく
TO_ADDRESS = ['xxxxxxx@hotmail.co.jp', 'yyyyyyyyyyyy@gmail.com']

def create_message(list_to_addr, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = FROM_NAME 
    msg['To'] = ','.join(list_to_addr)
    # よくわからないがBCCに入れてもBCCという欄に表示されるだけなので止める
    # msg['Bcc'] = ','.join(list_bcc_addrs)
    msg['Date'] = formatdate()
    return msg

def send_gmail(list_to_addr, msg):
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(FROM_ADDRESS, MY_PASSWORD)
    smtpobj.sendmail(FROM_ADDRESS, list_to_addr, msg.as_string())
    smtpobj.close()

def Notice_Mail(subject, send_message):
  list_to_addr = TO_ADDRESS
  msg = create_message(list_to_addr, subject, send_message)
  send_gmail(list_to_addr, msg)

line_notify_token = 'xxxxxxxxxxx'
def Notice_LINE_Self(send_message):
  line_notify_api = 'https://notify-api.line.me/api/notify'

  payload = {'message': send_message}
  headers = {'Authorization': 'Bearer ' + line_notify_token}
  line_notify = requests.post(line_notify_api, data=payload, headers=headers)

_access_token ='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
def Notice_LINE_push(to_user_id, send_message):

  # HTTPヘッダを設定
  header = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + _access_token,
  }

  # 送信データを設定
  send_data = {
      'to': to_user_id,
      'messages': [
          {
              'type': 'text',
              'text': send_message
          }
      ]
  }

  # 実行
  url = 'https://api.line.me/v2/bot/message/push'
  res = requests.post(url, headers=header, data=json.dumps(send_data))
  if(res.status_code != 200):
    print("error : [{}]".format(res.text))

slack_url = 'https://hooks.slack.com/services/xxxxxxxx/xxxxxxxx/xxxxxx'
def Notice_Slack(send_message):
  requests.post(slack_url, data=json.dumps({'text': send_message}))

teams_webhook_url = 'https://outlook.office.com/webhook/xxxxxxx/IncomingWebhook/xxxxxxx/xxxxxx'
def Notice_TEAMS(subject, send_message):
  send_message = send_message.replace('\n', '<BR>')
  requests.post(teams_webhook_url, data=json.dumps({'title': subject, 'text': send_message}))

url_ifttt = 'https://maker.ifttt.com/trigger/eventid/with/key/xxxxx'
def Notice_IFTTT(subject, send_message):
  requests.post(url_ifttt, data={'value1': subject, 'value2': send_message, 'value3': ''})

def Notice(subject, body):
  # 通知処理：メール
  Notice_Mail(subject, body)

  # 通知処理：LINE_Notify
  Notice_LINE_Self(body)

  # 通知処理：LINE_push
  userid = 'xxxxxxxxxx'
  Notice_LINE_push(userid, body)

  # 通知処理：Slack
  Notice_Slack(body)

  # 通知処理：TEAMS
  Notice_TEAMS(subject, body)

  # 通知処理：IFTTT（経由でLINEへ）
  Notice_IFTTT(subject, body)


import datetime
dt_now = datetime.datetime.now()

# 改行は\nで設定すればよい
body = "送信内容ですよ\n改行は反映されるのでしょうか？\n{}"
body = body.format(dt_now.strftime('%Y年%m月%d日 %H:%M:%S'))

subject = "＜通知サンプルですよ : {}＞".format(dt_now.strftime('%Y%m%d %H%M%S'))

# 通知
Notice(subject, body)
