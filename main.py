import functions_framework
from flask import Flask, request,escape
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage   # 載入 TextSendMessage 模組
import json
import pymysql

def get_token(user_msg):
    user_msg+=" "
    arr=[]
    l,r=0,0
    inNum=False
    for i in range(len(user_msg)):
        if user_msg[i].isdigit() and inNum==False:
            l=i
            inNum=True
        elif (not user_msg[i].isdigit() ) and inNum==True:
            r=i
            arr.append(user_msg[l:r])
            inNum = False
    return arr

def bot_speeking(tk,msg):
    line_bot_api = LineBotApi('')# fill api
    text_message = TextSendMessage(text=msg)  # 設定回傳同樣的訊息
    line_bot_api.reply_message(tk, text_message)  # 回傳訊息

@functions_framework.http
def hello_http(request):
    connection = pymysql.connect(unix_socket='/cloudsql/',#name
                                 user='',
                                 password='',
                                 database='',
                                 charset='',
                                )
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    with connection:
        with connection.cursor() as cursor:
            try:
                handler = WebhookHandler('')##webhook
                signature = request.headers['X-Line-Signature']
                handler.handle(body, signature)
                tk = json_data['events'][0]['replyToken']         # 取得 reply token
                user_msg = json_data['events'][0]['message']['text']   # 取得使用者發送的訊息
                user_msg = user_msg.lower()
                ###condition1
                if "token list" in user_msg:
                    sql="truncate table token;"
                    cursor.execute(sql)
                    for i in get_token(user_msg):
                        sql="INSERT INTO token VALUES ('"+i+"',null,null);"
                        cursor.execute(sql)
                ###condition2
                elif "nokia" in user_msg and "disconnect" in user_msg and "extend" not in user_msg:
                    sql = "select tokenID from token;"
                    cursor.execute(sql)
                    tokens = [i[0] for i in cursor.fetchall()]
                    try:

                        for token in tokens:
                            if token in get_token(user_msg):
                                sql = "update token set disconnect='True' where tokenID='"+token+"';"
                                cursor.execute(sql)
                                sql = "select tokenID from token where disconnect is null;"
                                cursor.execute(sql)
                                linking_token = [i[0] for i in cursor.fetchall()]
                                if not linking_token:
                                    bot_speeking(tk,str(len(linking_token))+" token(s) not disconnected")

                        else:
                            pass
                    except:
                        pass
                ###condition3
                elif "nokia" in user_msg and "connect" in user_msg and "user_msg" not in user_msg:
                    sql = "select tokenID from token;"
                    cursor.execute(sql)
                    tokens = [i[0] for i in cursor.fetchall()]
                    try:
                        for token in tokens:
                            if token in get_token(user_msg):
                                sql = "update token set connected='True',disconnect=NULL where tokenID='" + token + "';"
                                cursor.execute(sql)
                        else:
                            pass
                    except:
                        pass
                ###condition4
                elif "show linking" in user_msg:
                    sql = "select tokenID from token where disconnect is null;"
                    cursor.execute(sql)
                    linking_token = [i[0] for i in cursor.fetchall()]
                    # if linking_token:
                    bot_speeking(tk,str(len(linking_token))+" token(s) not disconnected")
                    # else:
                    #     bot_speeking(tk,"all disconnected")
                connection.commit()
            except Exception as e:
                print(e)
    return 'OK'