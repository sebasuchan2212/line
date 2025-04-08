from flask import Flask, request, abort
import requests
import json
import os
import logging  # ← ロギング追加

app = Flask(__name__)

# ロギング設定（Renderのログにもちゃんと出すため）
logging.basicConfig(level=logging.DEBUG)

# 環境変数からトークン取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_TOKEN"]
OPENROUTER_API_KEY = os.environ["OPENROUTER_KEY"]

LINE_REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
}


# 🔍 GPTへメッセージを送る関数（ログ付き）
def chat_with_gpt(user_message):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openai/gpt-3.5-turbo",  # または "openrouter/openai/gpt-3.5-turbo" に変更してもOK
        "messages": [
            {"role": "system", "content": "あなたは親切なLINEボットです。"},
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    try:
        res_json = response.json()
        app.logger.error("OpenRouterステータスコード: %s", response.status_code)
        app.logger.error("OpenRouterレスポンス: %s", res_json)

        if 'choices' in res_json:
            return res_json['choices'][0]['message']['content']
        elif 'error' in res_json:
            return f"OpenRouterエラー: {res_json['error']}"
        else:
            return "エラー：応答形式が不正です。"

    except Exception as e:
        app.logger.error("OpenRouterから例外が発生: %s", e)
        app.logger.error("レスポンス内容: %s", response.text)
        return "ごめん、AIからの返事がうまく届かなかったよ！"


# 🔁 LINEのWebhook
@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.json
    for event in body['events']:
        if event['type'] == 'message' and event['message']['type'] == 'text':
            user_msg = event['message']['text']
            reply_msg = chat_with_gpt(user_msg)
            payload = {
                "replyToken": event['replyToken'],
                "messages": [{"type": "text", "text": reply_msg}]
            }
            requests.post(LINE_REPLY_ENDPOINT, headers=HEADERS, data=json.dumps(payload))
    return 'OK'
