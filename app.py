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

        app.logger.error("OpenRouterステータスコード: %s", response.status_code)
        app.logger.error("OpenRouterレスポンス: %s", res_json)

        if 'choices' in res_json:
            return res_json['choices'][0]['message']['content']
        elif 'error' in res_json:
            return f"【エラー】{res_json['error'].get('message', '詳細不明')}"
        else:
            return "【エラー】OpenRouterから予期しない形式の返答がきました"

    except Exception as e:
        app.logger.error("OpenRouterで例外が発生: %s", e)
        app.logger.error("レスポンス内容: %s", response.text)
        return "【例外発生】AIからの返答に問題が発生しました…！"

