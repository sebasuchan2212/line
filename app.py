import logging
import json
import requests
from flask import Flask

app = Flask(__name__)

# ロギング設定
logging.basicConfig(level=logging.DEBUG)

def chat_with_gpt(user_message):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "あなたは親切なLINEボットです。"},
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        res_json = response.json()
        app.logger.debug("OpenRouterステータスコード: %s", response.status_code)
        app.logger.debug("OpenRouterレスポンス: %s", json.dumps(res_json, indent=2, ensure_ascii=False))

        if 'choices' in res_json:
            return res_json['choices'][0]['message']['content']
        elif 'error' in res_json:
            error_message = res_json['error'].get('message', '詳細不明')
            app.logger.error("OpenRouterエラー: %s", error_message)
            return f"〖エラー〗{error_message}"
        else:
            app.logger.error("OpenRouterから予期しない形式の返答がありました。")
            return "〖エラー〗OpenRouterから予期しない形式の返答がきました"

    except Exception as e:
        app.logger.exception("OpenRouterで例外が発生しました。")
        return "〖例外発生〗AIからの返答に問題が発生しました…！"


