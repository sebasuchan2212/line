def chat_with_gpt(user_message):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer " + OPENROUTER_API_KEY,
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
        print("OpenRouterのレスポンス:", res_json)

        return res_json['choices'][0]['message']['content']
    except Exception as e:
        print("OpenRouterからエラーが返ってきました:", response.text)
        return "ごめん、AIの応答で問題が起きたよ…！"
