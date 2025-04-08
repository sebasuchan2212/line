from flask import Flask, request, abort
import requests
import json
import os

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_TOKEN"]
LINE_REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
}

# OpenRouter API設定（無料枠あり）
OPENROUTER_API_KEY = os.environ["OPENROUTER_KEY"]
def chat_with_gpt(user_message):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": user_message}]
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()['choices'][0]['message']['content']

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
  
