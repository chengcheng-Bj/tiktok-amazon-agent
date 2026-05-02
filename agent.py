import os
import requests
import time

print("Agent started")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def ask_ai():
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": "Give 1 trending Amazon product idea for TikTok selling"}
                ]
            }
        ]
    }

    for i in range(3):
        try:
            r = requests.post(url, json=payload, timeout=20)
            data = r.json()

            print("RAW RESPONSE:", data)

            if "error" in data:
                return f"Gemini API ERROR: {data['error']}"

            if "candidates" not in data:
                return f"No candidates returned: {data}"

            return data["candidates"][0]["content"]["parts"][0]["text"]

        except Exception as e:
            print(f"Attempt {i+1} failed:", repr(e))

    return "AI ERROR: Gemini failed"

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    try:
        requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text
        }, timeout=10)
    except Exception as e:
        print("Telegram error:", e)


if __name__ == "__main__":
    result = ask_ai()
    print(result)
    send_telegram(result)
