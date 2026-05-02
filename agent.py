import os
import requests
from openai import OpenAI

print("Agent started")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

client = OpenAI(api_key=OPENAI_API_KEY)

def ask_ai():
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a cross-border e-commerce assistant."},
                {"role": "user", "content": "Give 1 trending Amazon product idea for TikTok."}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI ERROR: {str(e)}"

def send_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text
        })
    except Exception as e:
        print("Telegram error:", e)

if __name__ == "__main__":
    result = ask_ai()
    print(result)
    send_telegram(result)
