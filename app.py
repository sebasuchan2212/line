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

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    try:
        res_json = response.json()
        app.logger.error("OpenRouterのステータスコード: %s", response.status_code)
        app.logger.error("OpenRouterのレスポンス: %s", res_json)

        if 'choices' in res_json:
            return res_json['choices'][0]['message']['content']
        elif 'error' in res_json:
            return f"OpenRouterエラー: {res_json['error']}"
        else:
            return "エラー：応答形式が不正です。"

    except Exception as e:
        app.logger.error("OpenRouterから例外が発生: %s", str(e))
        app.logger.error("レスポンス内容: %s", response.text)
        return "ごめん、AIからの返事うまく届かなかったよ！"
