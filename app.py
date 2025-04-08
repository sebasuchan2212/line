def chat_with_gpt(user_message):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer " + OPENROUTER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openrouter/openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "あなたは親切なLINEボットです。"},
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    try:
        res_json = response.json()
        print("OpenRouterのステータスコード:", response.status_code)
        print("OpenRouterのレスポンス:", res_json)

        if "choices" in res_json:
            return res_json["choices"][0]["message"]["content"]
        elif "error" in res_json:
            return f"OpenRouterエラー: {res_json['error']}"
        else:
            return "エラー: 応答の形式が不正です。"
    except Exception as e:
        print("OpenRouterから例外:", e)
        print("レスポンス内容:", response.text)
        return "ごめん、AIからの返事がうまく届かなかったよ！"

