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

        # ログを出す（render のログで確認できる）
        app.logger.error("OpenRouterステータスコード: %s", response.status_code)
        app.logger.error("OpenRouterレスポンス: %s", json.dumps(res_json, ensure_ascii=False))

        # 分岐して安全に取り出す
        if 'choices' in res_json:
            return res_json['choices'][0]['message']['content']
        elif 'error' in res_json:
            return f"❌ OpenRouterエラー: {res_json['error'].get('message', '詳細不明')}"
        else:
            return "❌ OpenRouterから不明な形式のレスポンスが返ってきました。"

    except Exception as e:
        app.logger.exception("OpenRouterで例外が発生: %s", e)
        return "⚠️ 例外が発生しました。AIの返事がうまく取れなかったよ。"
