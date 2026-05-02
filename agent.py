import os
import requests
from openai import OpenAI

print("Agent started")

# ===== ENV =====
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ===== AI CLIENT =====
client = OpenAI(api_key=OPENAI_API_KEY)

# ===== 1. 调用 AI =====
def ask_ai():
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a cross-border e-commerce research assistant."},
            {"role": "user", "content": "Give me 1 trending Amazon product idea for TikTok selling."}
        ]
    )
    return response.choices[0].message.content

# ===== 2. 发送 Telegram =====
def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    requests.post(url, json=payload)

# ===== MAIN =====
if __name__ == "__main__":
    result = ask_ai()
    send_telegram(result)
    print("Done")
