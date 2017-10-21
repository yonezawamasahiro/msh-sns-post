import os

# web app framework
from flask import Flask, request, abort

# LINE api
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# docomo api
import doco.client


# set web server
app = Flask( __name__ )

# set LINE api
line_bot_api = LineBotApi( os.environ[ 'LINE_Channel_Access_Token' ] )
handler = WebhookHandler( os.environ[ 'LINE_Channel_Secret' ] )


# run when accessing "/callback" (flask)
@app.route( "/callback", methods = [ 'POST' ] )
def callback():

    # get X-Line-Signature header value
    # set LINE Signature
    signature = request.headers[ 'X-Line-Signature' ]

    # get request body as text
    # set LINE Message
    body = request.get_data( as_text = True )

    # handle webhook body
    # (def handle_text_message)
    try:
        handler.handle( body, signature )
    except InvalidSignatureError:
        abort( 400 )
    return 'OK'


# run when adding values to "handler" (flask)
@handler.add( MessageEvent, message = TextMessage )
def handle_text_message( event ):

    # text from user
    text = event.message.text

    # send text (docomo api) to LINE api
    line_bot_api.reply_message( event.reply_token, TextSendMessage( text = text ) )


# can't use "app.py" as an import module
if __name__ == "__main__":
    app.run( host='0.0.0.0', port=os.environ[ 'PORT' ] )
