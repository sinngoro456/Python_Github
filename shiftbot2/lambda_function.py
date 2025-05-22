import os
import logging
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage  # 追加インポート
from linebot.exceptions import InvalidSignatureError
from main import handle_text

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

# LINE Botの設定
channel_secret = os.getenv("LINE_CHANNEL_SECRET")
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

if not channel_secret or not channel_access_token:
    logger.error("LINEチャネルのシークレットまたはアクセストークンが設定されていません")
    raise ValueError("LINEチャネルのシークレットまたはアクセストークンが設定されていません")

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

def lambda_handler(event, context):
    # 署名検証用のヘッダーとボディを取得
    signature = event["headers"]["x-line-signature"]
    body = event["body"]

    # 成功時のレスポンス
    ok_response = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {},
        "body": ""
    }

    # エラー時のレスポンス
    error_response = {
        "isBase64Encoded": False,
        "statusCode": 500,
        "headers": {},
        "body": "Error"
    }

    @handler.add(MessageEvent, message=TextMessage)
    
    def handle_message(event):
        # 受信したメッセージをそのまま返信
        received_text = event.message.text
        output_text = handle_text(received_text)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=output_text)
        )
        
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return error_response
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return error_response

    return ok_response