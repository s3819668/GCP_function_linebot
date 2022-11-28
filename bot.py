from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('FASQranQdZbYetlCh9+UihjZaAgplxjBwr6AE4dYd9uHhFqySIJWCtBvmqk+F/V9KDYB+w+uLy2s3wyPFOoqAsPKLBfA5jvXEDj8gKd3vUHj3XrANEa5YJ9gm8rfTlXHWVfTF53DBdm4x2z8UOV9IwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('8b36afc8501f4b0c4292dd48358d30d1')


@app.route("/callback", methods=['POST']) ## 接 POST 需求
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature) ## 丟到 Handler 去處理訊息
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)) ## 回傳 User 剛剛所傳的訊息 (Echo Bot)
    print(event.message.text)


if __name__ == "__main__":
    app.run()